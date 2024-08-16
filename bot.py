import os
import subprocess


import nextcord
from nextcord.ext import commands

from card_game import Card, CardGame
from wwnames import WildWestNames

bot = commands.Bot()
git_sha = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
card_game = CardGame()


@bot.event
async def on_ready():
    print('Howdy folks.')


@bot.slash_command(description='Version')
async def wwname_version(interaction: nextcord.Interaction):
    await interaction.send(git_sha)


@bot.slash_command(description='Generate a name')
async def wwname(interaction: nextcord.Interaction, gender: str = '', number: int = 1):
    names = WildWestNames()
    await interaction.send(names.random_name(gender, number))


@bot.slash_command(description='Deal a card to a player')
async def deal_hand(interaction: nextcord.Interaction, number: int = 1, player: str = ''):
    # If player is not given, use the interaction author
    if player == '':
        player = interaction.user.name
    card_game.deal(player, number)
    await interaction.send(f'{player} was dealt {number} cards.')


@bot.slash_command(description='Deal a card to all players')
async def deal_all(interaction: nextcord.Interaction, number: int = 1):
    card_game.deal_all(number)
    await interaction.send(f'All players were dealt {number} cards.')


@bot.slash_command(description='Discard a card from a player')
async def discard(interaction: nextcord.Interaction, card_value: str, card_suit: str, player: str = ''):
    if player == '':
        player = interaction.user.name
    card = Card(card_suit, int(card_value))
    card_game.discard(player, card)
    await interaction.send(f'{player} discarded {card}.')


@bot.slash_command(description='Discard all cards from all players')
async def discard_all(interaction: nextcord.Interaction):
    card_game.discard_all()
    await interaction.send('All cards were discarded.')


@bot.slash_command(description='Shuffle the deck')
async def shuffle_deck(interaction: nextcord.Interaction):
    card_game.shuffle()
    await interaction.send('The deck was shuffled.')


@bot.slash_command(description='Show a player\'s hand')
async def show_hand(interaction: nextcord.Interaction, player: str = ''):
    if player == '':
        player = interaction.user.name
    hand = card_game.hands.get(player, [])
    await interaction.send(f'{player}\'s hand: {", ".join(str(card) for card in hand)}')


bot.run(os.getenv('DISCORD_TOKEN'))
