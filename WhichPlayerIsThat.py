#WhichPlayerIsThat Code

import discord
from discord.ext import commands
import requests 
from bs4 import BeautifulSoup

# Initialize bot
bot = commands.Bot(command_prefix='!')

# Command to get player stats
@bot.command()
async def playerstats(ctx, *, player_name):
    # Query Baseball Reference
    url = f'https://www.baseball-reference.com/search/search.fcgi?search={player_name.replace(" ", "+")}'
    response = requests.get(url)
    if response.status_code == 200:
        # Parse HTML response
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find player page link
        player_link = soup.find('a', {'class': 'search-item-name'})['href']
        player_url = f'https://www.baseball-reference.com{player_link}'
        player_response = requests.get(player_url)
        if player_response.status_code == 200:
            player_soup = BeautifulSoup(player_response.text, 'html.parser')
            # Extract player stats
            stats_table = player_soup.find('table', {'id': 'batting_standard'})
            if stats_table:
                stats_rows = stats_table.find_all('tr')[1:]  # Exclude header row
                player_stats = ''
                for row in stats_rows:
                    columns = row.find_all(['th', 'td'])
                    year = columns[0].get_text()
                    team = columns[1].get_text()
                    player_stats += f'{year} - {team}: {columns[6].get_text()}\n'  # Example: 2023 - New York Yankees: .300/.400/.500
                await ctx.send(f'**{player_name} Stats:**\n```{player_stats}```')
            else:
                await ctx.send('Player stats not found.')
        else:
            await ctx.send('Failed to fetch player data.')
    else:
        await ctx.send('Failed to search for the player.')

# Run the bot
bot.run('MTIwMzExNjYzOTQzNzA2NjI0MA.GNwInS.lSHX_-3Ddt9wwk9VRma8ZqDl9mu7rizwB6-qoY')