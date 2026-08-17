import discord
from discord.ext import commands
from discord import app_commands
from typing import List
import asyncio
import logging

from config import DISCORD_TOKEN, REGIONS, TIME_FORMAT_EXAMPLES
from availability_manager import AvailabilityManager
from time_parser import TimeParser

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RegionDropdown(discord.ui.Select):
    """Dropdown menu for region selection."""

    def __init__(self, availability_manager: AvailabilityManager):
        self.availability_manager = availability_manager

        # Create options for the dropdown
        options = [
            discord.SelectOption(label=region, value=region)
            for region in REGIONS
        ]

        super().__init__(placeholder="Choose your region...",
                         min_values=1,
                         max_values=1,
                         options=options)

    async def callback(self, interaction: discord.Interaction):
        """Handle region selection."""
        selected_region = self.values[0]

        # Store the user's region choice
        if interaction.guild:
            self.availability_manager.set_user_region(interaction.guild.id,
                                                      interaction.user.id,
                                                      selected_region)

        embed = discord.Embed(
            title="Region Selected!",
            description=f"You have selected: **{selected_region}**",
            color=discord.Color.green())
        embed.add_field(
            name="Next Step",
            value="Use `/set_availability` to set your available hours!",
            inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


class RegionView(discord.ui.View):
    """View containing the region dropdown."""

    def __init__(self, availability_manager: AvailabilityManager):
        super().__init__(timeout=300)  # 5 minute timeout
        self.add_item(RegionDropdown(availability_manager))


class AvailabilityBot(commands.Bot):
    """Discord bot for coordinating available time sessions."""

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True

        super().__init__(command_prefix='!', intents=intents)

        self.availability_manager = AvailabilityManager()
        self.time_parser = TimeParser()

    async def setup_hook(self):
        """Called when the bot is ready to sync commands."""
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")

    async def on_ready(self):
        """Called when bot is ready."""
        logger.info(f'{self.user} has connected to Discord!')
        logger.info(f'Bot is in {len(self.guilds)} guilds')


# Initialize bot
bot = AvailabilityBot()


# Function to send personalized messages
async def send_personalized_messages(guild_id: int,
                                     channel,
                                     min_players: int = 2):
    """Send personalized optimal times to each user in their own timezone."""
    guild_users = bot.availability_manager.get_all_users_in_guild(guild_id)

    # Get users who have set both region and availability
    active_users = {}
    for user_id, data in guild_users.items():
        if 'region' in data and 'availability' in data and data['availability']:
            active_users[user_id] = data

    if len(active_users) < min_players:
        return

    # Calculate UTC optimal times once
    utc_optimal_times = bot.availability_manager.calculate_optimal_times(
        guild_id, min_players)

    if not utc_optimal_times:
        return

    # Send personalized messages to each active user
    for user_id, user_data in active_users.items():
        try:
            user = await bot.fetch_user(user_id)
            user_region = user_data.get('region', 'UTC')

            # Convert UTC times to user's timezone
            local_optimal_times = []
            for utc_start, utc_end, count, user_ids in utc_optimal_times:
                local_start = bot.availability_manager.convert_utc_to_local(
                    utc_start, user_region)
                local_end = bot.availability_manager.convert_utc_to_local(
                    utc_end, user_region)

                # Handle day boundary crossing
                if local_start > local_end:
                    local_optimal_times.append(
                        (local_start, 24.0, count, user_ids))
                    local_optimal_times.append(
                        (0.0, local_end, count, user_ids))
                else:
                    local_optimal_times.append(
                        (local_start, local_end, count, user_ids))

            # Create personalized message
            times_embed = discord.Embed(
                title=f"Your Optimal Play Times ({user_region} Time)",
                color=discord.Color.green())

            times_text = []
            for i, (start, end, count,
                    user_ids) in enumerate(local_optimal_times[:3]):
                start_formatted = bot.time_parser._format_time_float(start)
                end_formatted = bot.time_parser._format_time_float(end)
                times_text.append(
                    f"# {start_formatted}-{end_formatted} ({count} players)")

            times_embed.description = "\n".join(times_text)
            times_embed.set_footer(
                text=f"Times shown in {user_region} timezone")

            # Send message in channel with user mention
            await channel.send(f"{user.mention}", embed=times_embed)

        except Exception as e:
            print(f"Error sending personalized times to user {user_id}: {e}")


@bot.tree.command(name="choose_region",
                  description="Select your region from a dropdown menu")
async def choose_region(interaction: discord.Interaction):
    """Slash command to show region selection dropdown."""

    embed = discord.Embed(
        title="🌍 Select Your Region",
        description=
        "Choose your preferred region from the dropdown below:",
        color=discord.Color.blue())
    embed.add_field(name="Available Regions",
                    value="\n".join([f"• {region}"
                                     for region in REGIONS[:5]]) +
                    f"\n... and {len(REGIONS)-5} more",
                    inline=False)

    view = RegionView(bot.availability_manager)
    await interaction.response.send_message(embed=embed,
                                            view=view,
                                            ephemeral=True)


@bot.tree.command(name="set_availability",
                  description="Set your available hours")
@app_commands.describe(
    times="Your available times (e.g., 'Not Available', '3-4', '5-8, 4-5')")
async def set_availability(interaction: discord.Interaction, times: str):
    """Slash command to set user availability."""

    try:
        if not interaction.guild:
            await interaction.response.send_message(
                "This command can only be used in a server.", ephemeral=True)
            return

        # Validate and store availability
        bot.availability_manager.set_user_availability(interaction.guild.id,
                                                       interaction.user.id,
                                                       times)

        # Get user's current data
        user_data = bot.availability_manager.get_user_data(
            interaction.guild.id, interaction.user.id)

        region = user_data.get('region', 'Not Set')
        local_availability = user_data.get('local_availability', [])

        # Format response
        if local_availability:
            formatted_times = bot.time_parser.format_time_ranges(
                local_availability)
            embed = discord.Embed(
                title="✅ Availability Set!",
                description=f"Your availability has been updated.",
                color=discord.Color.green())
        else:
            formatted_times = "Not Available"
            embed = discord.Embed(
                title="✅ Availability Set!",
                description=f"You are marked as not available.",
                color=discord.Color.orange())

        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Available Times",
                        value=formatted_times,
                        inline=True)

        # Check if we should calculate optimal times
        guild_users = bot.availability_manager.get_all_users_in_guild(
            interaction.guild.id)
        users_with_availability = bot.availability_manager.users_with_availability_count(
            interaction.guild.id)

        if users_with_availability >= 2:
            embed.add_field(
                name="Status",
                value=
                f"{users_with_availability} members have set availability. Calculating optimal times...",
                inline=False)

            # Send the main response first
            await interaction.response.send_message(embed=embed)

            # Send personalized optimal times to each user in their timezone
            await send_personalized_messages(interaction.guild.id,
                                             interaction.channel,
                                             min_players=2)
            return

        await interaction.response.send_message(embed=embed)

    except ValueError as e:
        # Handle invalid time format
        embed = discord.Embed(title="❌ Invalid Time Format",
                              description=str(e),
                              color=discord.Color.red())
        embed.add_field(name="Valid Formats",
                        value="\n".join([
                            f"• `{example}`"
                            for example in TIME_FORMAT_EXAMPLES
                        ]),
                        inline=False)
        embed.add_field(
            name="Examples",
            value=
            "• `Not Available` - You're not available\n• `14-16` - Available from 2 PM to 4 PM\n• `12:30-13:15` - Available from 12:30 PM to 1:15 PM\n• `9:00-12:00, 18:30-20:00` - Available 9 AM-12 PM and 6:30-8 PM",
            inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(
    name="show_schedule",
    description="Show current schedule and optimal meet times for the server")
async def show_schedule(interaction: discord.Interaction):
    """Show the current schedule and calculate optimal meet times."""

    if not interaction.guild:
        await interaction.response.send_message(
            "This command can only be used in a server.", ephemeral=True)
        return

    guild_id = interaction.guild.id

    # Get guild summary
    summary = bot.availability_manager.get_guild_summary(guild_id)

    embed = discord.Embed(title="🗓️ Server Schedule",
                          description=summary,
                          color=discord.Color.blue())

    # Get user's timezone for displaying times
    user_data = bot.availability_manager.get_user_data(guild_id,
                                                       interaction.user.id)
    user_region = user_data.get('region', 'UTC')

    # Calculate optimal times in user's timezone
    optimal_times = bot.availability_manager.get_optimal_times_for_user(
        guild_id, interaction.user.id, min_players=2)

    if optimal_times:
        # Send the main response first
        await interaction.response.send_message(embed=embed)

        # Create a separate message for optimal play times with larger font
        times_embed = discord.Embed(
            title=f" Optimal Play Times ({user_region} Time)",
            color=discord.Color.green())

        # Use Discord's header formatting for larger text
        large_times_text = []
        for i, (start, end, count,
                user_ids) in enumerate(optimal_times[:5]):  # Show top 5 slots
            user_mentions = [f"<@{uid}>"
                             for uid in user_ids[:3]]  # Show first 3 users
            if len(user_ids) > 3:
                user_mentions.append(f"and {len(user_ids)-3} more")

            start_formatted = bot.time_parser._format_time_float(start)
            end_formatted = bot.time_parser._format_time_float(end)

            large_times_text.append(
                f"# {i+1}. {start_formatted}-{end_formatted} ({count} players)\n"
                f"Players: {', '.join(user_mentions)}")

        times_embed.description = "\n\n".join(large_times_text)
        await interaction.followup.send(embed=times_embed)
        return
    else:
        embed.add_field(
            name="✅ Optimal Time Slots",
            value=
            "No overlapping availability found. More members need to set their availability!",
            inline=False)

    # Add helpful footer
    embed.set_footer(
        text="Use /choose_region and /set_availability to join the schedule!")

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="clear_my_data",
                  description="Clear your region and availability data")
async def clear_my_data(interaction: discord.Interaction):
    """Clear user's own data."""

    if not interaction.guild:
        await interaction.response.send_message(
            "This command can only be used in a server.", ephemeral=True)
        return

    bot.availability_manager.clear_user_data(interaction.guild.id,
                                             interaction.user.id)

    embed = discord.Embed(
        title="🗑️ Data Cleared",
        description="Your region and availability data has been cleared.",
        color=discord.Color.orange())
    embed.add_field(
        name="Next Steps",
        value=
        "Use `/choose_region` and `/set_availability` to set your preferences again.",
        inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(
    name="help",
    description="Show help information for coordination commands")
async def help(interaction: discord.Interaction):
    """Show help information."""

    embed = discord.Embed(
        title="Availability Bot Help",
        description=
        "This bot helps coordinate meeting or activity times for groups...",
        color=discord.Color.purple())

    embed.add_field(name="📍 /choose_region",
                    value="Select your region or time zone",
                    inline=False)

    embed.add_field(
        name="⏰ /set_availability",
        value="Set your available hours\n"
        "**Examples:**\n"
        "• `Not Available` - You're not available\n"
        "• `14-16` - Available from 2 PM to 4 PM\n"
        "• `12:30-13:15` - Available from 12:30 PM to 1:15 PM\n"
        "• `9:00-12:00, 18:30-20:00` - Available 9 AM-12 PM and 6:30-8 PM",
        inline=False)

    embed.add_field(
        name="📋 /show_schedule",
        value="View current server schedule and optimal play times",
        inline=False)

    embed.add_field(name="🗑️ /clear_my_data",
                    value="Clear your region and availability data",
                    inline=False)

    embed.add_field(
        name="How It Works",
        value="1. Choose your region\n"
        "2. Set your availability\n"
        "3. Bot automatically calculates best times when multiple people have set availability\n"
        "4. View optimal play times that work for the most players!",
        inline=False)

    embed.set_footer(text="All times are in 24-hour format (0-23)")

    await interaction.response.send_message(embed=embed, ephemeral=True)


# Error handling
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction,
                               error: app_commands.AppCommandError):
    """Handle application command errors."""

    if isinstance(error, app_commands.CommandOnCooldown):
        embed = discord.Embed(
            title="⏱️ Command on Cooldown",
            description=
            f"Please wait {error.retry_after:.2f} seconds before using this command again.",
            color=discord.Color.orange())
    else:
        embed = discord.Embed(
            title="❌ An Error Occurred",
            description="Something went wrong. Please try again later.",
            color=discord.Color.red())
        logger.error(f"Command error: {error}")

    if not interaction.response.is_done():
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.followup.send(embed=embed, ephemeral=True)


# Run the bot
if __name__ == "__main__":
    if DISCORD_TOKEN == 'your_discord_bot_token_here':
        logger.error("Please set the DISCORD_TOKEN environment variable!")
        exit(1)

    try:
        bot.run(DISCORD_TOKEN)
    except discord.LoginFailure:
        logger.error(
            "Invalid Discord token. Please check your DISCORD_TOKEN environment variable."
        )
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
