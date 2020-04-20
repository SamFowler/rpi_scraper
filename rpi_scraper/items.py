# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

"""
Define the class models for scraped information
"""

from scrapy import Item, Field

class Season(Item):
	"""
		Data structure to store information about matches in each tournament season
	"""

	tournament = Field()
	season = Field()



class Match(Item):
	"""
		Data structure to store basic match info
	    (team1_id, team2_id, ground, winner, match_type, date, tournament, season)
	"""

	match_id = Field()

	home_team_id = Field()
	home_team_name = Field()
	away_team_id = Field()
	away_team_name = Field()

	status = Field()

	stadium = Field()
	winner = Field()
	match_type = Field()

	tournament = Field()
	season = Field()

	date = Field()
	start_time = Field()
	end_time = Field()
	performers = Field()
	description = Field()
	rugbypass_price = Field()
	rugbypass_price_curr = Field()
	comp = Field()
	comp_date = Field()
	score_home = Field()
	score_away = Field()
	title = Field()


	referee = Field()
	attendance = Field()

	tournament = Field()
	season = Field()

class MatchScore(Item):
	"""
		Data structure to store match stats
	"""

	match_id = Field()
	team_id = Field()

	points = Field()
	conceded = Field()

	tries = Field()
	conv_goals = Field()
	pen_goals = Field()
	drop_goals = Field()

	rpi_win_likelihood = Field()


class MatchStats(Item):
	"""
		Data structure to store detailed match stats
	"""

	match_id = Field()
	team_id = Field()


	points = Field()

	tries = Field()
	conv_goals = Field()
	pen_goals = Field()
	drop_goals = Field()

	rpi_win_likelihood = Field()


	#attack
	possession = Field()
	tries = Field()
	metres_carried = Field()
	carries = Field()
	defenders_beaten = Field()
	clean_breaks = Field()
	passes = Field()
	offloads = Field()
	turnovers_conceded = Field()

	#defence
	tackles = Field()
	tackles_missed = Field()
	turnovers_won = Field()

	#kicking
	kicks_in_play = Field()
	conversions = Field()
	conversions_missed = Field()
	pen_goals = Field()
	pen_goals_missed = Field()
	drop_goals = Field()
	drop_goals_missed = Field()

	#breakdown
	rucks_won = Field()
	rucks_lost = Field()
	rucks_won_pc = Field()
	mauls_won = Field()

	#set plays
	lineouts_won = Field()
	lineouts_lost = Field()
	lineouts_won_pc = Field()
	scrums_won = Field()
	scrums_lost = Field()
	scrums_won_pc = Field()

	#discipline
	pens_conceded = Field()
	red_cards = Field()
	yellow_cards = Field()


class Team(Item):
	"""
		Data structure to store team info
	"""

	team_id = Field()
	name = Field()

class Player(Item):
	"""
		Data structure to store player info
	"""

	player_id = Field()
	url_name = Field()
	full_name  = Field()
	birthday  = Field()
	height = Field()
	weight = Field()
	teams = Field()
	positions = Field()

class PlayerRPI(Item):
	"""
		Data structure to store player RugbyPassIndex info
	"""

	player_id = Field()
	date = Field()
	rpi = Field()
	core_stats = Field()

class PlayerStats(Item):
	"""
		Data structure to store player stats per match
	"""

	player_id = Field()
	team_id = Field()
	match_id = Field()
	position = Field()
	number = Field()
	starter = Field()
	tries = Field()
	cons = Field()
	pens = Field()
	drops = Field()

class PlayerExtraStats(Item):
	"""
		Data structure to store player detailed stats per match
	"""

	player_id = Field()
	team_id = Field()
	match_id = Field()

	minutes = Field()

	carries = Field()
	metres = Field()
	clean_breaks = Field()
	runs = Field()
	defenders_beaten = Field()

	tackles = Field()
	tackles_missed = Field()
	turnovers_won = Field()
	turnovers_conceder = Field()

	pens_conceded = Field()
	pens_conceded_atk = Field()
	pens_conceded_def = Field()
	yellow_cards = Field()
	red_cards = Field()
	
	passes = Field()
	offloads = Field()
	kicks_from_hand = Field()

	lineout_throw_won_clean = Field()
	lineout_throw_won = Field()
	lineout_won_steal = Field()

	points = Field()
	tries = Field()
	conv_goals = Field()
	pen_goals = Field()
	drop_goals = Field()
	try_assists = Field()

class GameEvent(Item):
	"""
		Data structure to store game events
	"""
	game_event_id = Field()
	player_id = Field()
	team_id = Field()
	match_id = Field()

	time = Field()
	action_type = Field()
	extra_info = Field()

class MatchFeedEvent(Item):
	"""
		Data structure to store live match feed
	"""

	match_id = Field()

	time = Field()
	game_event_id = Field()
	feed_contents = Field()


