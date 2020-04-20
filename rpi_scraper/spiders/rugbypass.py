# -*- coding: utf-8 -*-
import scrapy

from urllib.parse import urljoin

from scrapy.loader import ItemLoader

from rpi_scraper.items import Match, MatchScore, MatchStats, PlayerStats

import pandas as pd

class RugbypassSpider(scrapy.Spider):
	"""Main spider of the scraper."""

	#scrapy params
	name = 'rugbypass'
	allowed_domains = ['rugbypass.com']

	#custom params
	start_domain = 'https://www.rugbypass.com/'

	tournaments = ['internationals', 'premiership']#'currie-cup'] #, 'european-champions-cup', 'mitre-10-cup',
					#'pro-14', 'the-rugby-championship', 'rugby-world-cup', 
					#'sevens', 'six-nations', 'super-rugby', 'top-14']

	def get_tournament_url(self, tournament):
		#returns url to tournament page
		return urljoin(self.start_domain, f"{tournament}/matches")

	def start_requests(self):
		"""
			Method that initialises the spider. Sends requests to rugbypass tournament pages for 
			each tournament in class 'tournaments' variable.
			Sends requests to tournament urls e.g.: https://www.rugbypass.com/{tournament}/matches
		"""

		for tournament in self.tournaments:

			print(f"############### Sending initial request to tournament '{tournament}' page ###############")
			self.logger.info(f"############### Sending initial request to tournament '{tournament}' page ###############")

			yield scrapy.Request(
				url = self.get_tournament_url(tournament = tournament),
				callback = self.tournament_page_parse,
				meta = {'tournament': tournament}
				)


	def parse(self, response):
	    print('parse')

	def tournament_page_parse(self, response):
		"""
			Callback to handle parsing and processing of each tournament page
			Example url being parsed: https://www.rugbypass.com/{tournament}/matches
			Sends requests to parse the match list of each season of the tournament
		"""

		tournamet = response.meta['tournament']
		#print(f"	{response.url}")
		print(f"	Initialising parse for tournament '{tournamet}' page")
		self.logger.info(f"############### Initialising parse for tournament '{tournamet}' page ###############")

		# send request to parse the match list of each season of the tournament
		for season in response.css(".rounds-seasons.rounds-nav-select li a::text")[:2]:
			
			print(f"	  Sending request to parse match list of season '{season.get()}' in tournament '{tournamet}' page")
			self.logger.info(f"############### Sending request to parse match list of season '{season.get()}' in tournament '{tournamet}' page ###############")

			yield response.follow(
				url = f"matches/{season.get()}", 
				callback = self.season_matches_parse,
				dont_filter=True,
				meta = ({
						'tournament': tournamet, 
						 'season': season.get()
						 })
				)


	def season_matches_parse(self, response):
		"""
			Callback to handle parsing of the match list for each tournament season.
			Parses url such as https://www.rugbypass.com/{tournament}/matches/{season}
		"""
		#print(f"	    {response.url}")
		print(f"	    Parsing match list for tournament '{response.meta['tournament']}' in season '{response.meta['season']}'")
		#print(f"Tournament: {response.meta['tournament']}, season/year: {response.meta['season']}")
		self.logger.info(f"############### Parsing match list for tournament '{response.meta['tournament']}' in season '{response.meta['season']}' ###############")


		#css selectors for match details
		meta_fields = {
			'match_id': ' ::attr(data-id)',
			'date': ' ::attr(data-date)',
			'home_team_id': " ::attr(data-home)",
			#'home_team_name' : '',
			'away_team_id': " ::attr(data-away)",
			#'home_team_name': '',
			'status': " ::attr(data-status)",
			#'game_class': '',
			'start_time': " [itemprop='startDate']::attr(content)",
			'end_time': " [itemprop='endDate']::attr(content)",
			'performers': " [itemprop='performer']::attr(content)",
			'description': " [itemprop='description']::attr(content)",
			'rugbypass_price': " [itemprop='price']::attr(content)",
			'rugbypass_price_curr': " [itemprop='priceCurrency']::attr(content)",
			'title': "a.link-box::attr(href)",
			#'name': '',
			#'comp': '',
			#'comp_date': ''
			#'score_home': ''
			#'score_away': ''
		}

		

		match_ids = response.css("div[class=game-round] div[itemscope] ::attr(data-id)").getall()

		for match_id in match_ids[:1]:
		
			#Extract basic match information into Match container
			loader = ItemLoader(item=Match(), response=response)
			#loader to handle each match listed on the season page individually
			match_loader = loader.nested_css(f"[data-id='{match_id}']")
			for field, selector in meta_fields.items(): 
				#load css selector for match details 
				match_loader.add_css(field, selector)

			match_loader.add_value('tournament', response.meta['tournament'])
			match_loader.add_value('season', response.meta['season'])
			#fetch match data
			match = match_loader.load_item()


			#Send request to parsed match page
			url = response.css(f"[data-id='{match_id}'] a.link-box::attr(href)").get()
			#print('url: ', urljoin(url, f"{response.meta['season']}/stats"))
			yield response.follow(
				url = urljoin(url, f"{response.meta['season']}/stats"),
				callback = self.match_stats_page_parse,
				meta = ({
						'match': match,
						 })
				) 
			

		
			

		##Could request match per iteration above, or get full list by:
		#

		#Send requests to team pages. Could do this later to save requesting the same team multiple times?
		#team_page_urls = set(response.css("a.name.team-link::attr(href)").getall())#
		#for team_page_url in team_page_urls:
			#print(f"{team_page_url}/statistics")
			#if 'teams' in team_page_url.split('/')[-1]:
			#	continue
		#	yield response.follow(
		#		url = f"{team_page_url}/statistics",
		#		callback = self.team_page_parse,
				#dont_redirect=True,
		#		meta = {'url': team_page_url}
		#	) 



	def match_page_parse(self, response):
		"""
			Callback function to handle parsing of base match page. Also sends requests to
			match stats and info pages.
			Example url parsed: https://www.rugbypass.com/live/{tournament}/{match_name}/{season}
		"""

		url_desc = (" ".join(response.url.split('/')[-2].split('-')))
		print(f"		  Parsing match coverage page: {url_desc}")
		self.logger.info(f"############### Parsing match coverage page: {url_desc} ###############")

		#Add to basic match info
		match = response.meta['match']
		match['stadium'] = " ".join(response.url.split('/')[-2].split('-at-')[1].split('-on-')[0].split('-'))
		match['home_team_name'] =  " ".join(response.url.split('/')[-2].split('-at-')[0].split('-vs-')[0].split('-'))
		match['away_team_name'] =  " ".join(response.url.split('/')[-2].split('-at-')[0].split('-vs-')[1].split('-'))
		#" ".join(response.url.split('/')[-2].split('-at-')[0].split('vs')[1].split('-'))
		print(match)





		yield response.follow(
			url = urljoin(response.meta['url'], 'info'),
			callback = self.match_info_page_parse,
			#dont_filter=True,
			) 

		#yield response.follow(
		#	url = urljoin(response.meta['url'], 'stats'),
		#	callback = self.match_stats_page_parse,
		#	dont_filter=True,
		#	)




	def match_info_page_parse(self, response):
		"""

		"""
		print(f"       Parsing match info page")#: {response.meta['match']['description'][0]}")
		#self.logger.info(f"############### Parsing match page:  {response.meta['match']['description'][0]} ###############")


	circle_graph_titles = {
				'Possession': 'possession',
				'Tries': 'tries',
				'Passes': 'passes',
				'Tackles': 'tackles',
				'Kicks in play': 'kicks_in_play',
				'Conversions': 'conv_goals',
				'Rucks won': 'rucks_won',
				'Rucks lost': 'rucks_lost',
			}

	stat_bar_titles = {
				'Metres carried': 'metres_carried',
				'Carries': 'carries',
				'Defenders beaten': 'defenders_beaten',
				'Clean breaks': 'clean_breaks',
				'Offloads': 'offloads',
				'Turnovers conceded': 'turnovers_conceded',
				'Missed tackles': 'tackles_missed',
				'Turnovers won': 'turnovers_won',
				'Conversions missed': 'conversions_missed',
				'Penalty goals': 'pen_goals',
				'Penalty goals missed': 'pen_goals_missed',
				'Drop goals': 'drop_goals',
				'Drop goals missed': 'drop_goals_missed',
				'Rucks won %': 'rucks_won_pc',
				'Mauls won': 'mauls_won',
				'Lineouts won': 'lineouts_won',
				'Lineouts lost': 'lineouts_lost',
				'Lineouts won %': 'lineouts_won_pc',
				'Scrums won': 'scrums_won',
				'Scrums lost': 'scrums_lost',
				'Scrums won %': 'scrums_won_pc',
				'Penalties conceded': 'pens_conceded',
				'Red cards': 'red_cards',
				'Yellow cards': 'yellow_cards'
				}

	def match_stats_page_parse(self, response):
		"""
			Callback function to handle parsing of match STATS page.
			Example url parsed: https://www.rugbypass.com/live/{tournament}/{match_name}/{season}/stats
		"""
		match = response.meta['match']
		print(f"		  {response.url}")
		print(f"		  [{match['match_id'][0]}] Parsing match stats page")
		self.logger.info(f"############### [{match['match_id'][0]}]Parsing match stats page ###############")


		#Extract basic match information into Match container

		##Todo: check for "Sorry no stats available"

		for index, team_id in enumerate([match['home_team_id'], match['away_team_id']]):


			####### Collect match stats #######
			#Create MatchStats loader
			stats_loader = ItemLoader(item=MatchStats(), response=response)
			stats_loader = stats_loader.nested_css(f"[data-id='{match['match_id'][0]}']")
			stats_loader.add_value('team_id', team_id[0])
			stats_loader.add_value('match_id', match['match_id'])

			# 1) Collect match stats from circle graphs on match stats page
			team_is_away_team = index
			for res in response.css("script::text"): 
				if 'CirclesGraph' in res.get():
					graph_details = res.get().replace(" window.scriptsToInit.push('new CirclesGraph(", '').split("\"team-")
					for graph in graph_details[1:]:
						graph_split = graph.split(',')
						stats_loader.add_value(
							self.circle_graph_titles[graph_split[1].strip("\"")], 
							graph_split[1].strip("\"")
						)

			# 2) Collect match stats from stat bar "graphs" on match stats page
			home_or_away = 'home' if index==0 else 'away'
			stat_bars = response.css("div.stat-bars-item")
			for stat_bar in stat_bars:
				bar_text = stat_bar.css("div.label::text").get().strip()
				if bar_text in self.stat_bar_titles:
					stats_loader.add_value(
						self.stat_bar_titles[bar_text], 
						stat_bar.css(f"div.{home_or_away}::text").get()
						)

			match_stats = stats_loader.load_item()
			#print(match_stats)
			print(f"		  [{match['match_id'][0]}][{team_id[0]}] Created and filled MatchStats object")
			self.logger.info(f"############### [{match['match_id'][0]}][{team_id[0]}] Created and filled MatchStats object ###############")


			####### Collect player stats #######
			# Create player stats loader 

			player_stats_sel = response.css(f"div.match-centre-stats-page-team.{home_or_away}.full-player-stats")
			#print(player_stats_sel.css('table[data-index]').get())
			#print(len(player_stats_sel.css('table[data-index]')))
			stat_tables = []
			team_name = ''
			for index, stat_table in enumerate(player_stats_sel.css('table[data-index]')):
				#print(stat_table, '\n')
				#print(pd.read_html(stat_table.get(), index_col=1)[0], '\n')
				df = pd.read_html(stat_table.get())[0]
				if index != 0:
					df.drop([df.keys()[0], df.keys()[1]], axis=1, inplace=True)
				

				stat_tables.append(df)



			#print((stat_tables[0].keys()))
			#df = pd.DataFrame.from_records(stat_tables)
			df = pd.concat(stat_tables, axis=1)
			df.rename(columns={df.keys()[0]: 'ShirtNumber',
								df.keys()[1]: 'PlayerName'
								},
								inplace=True
								)
			df = df.dropna().reset_index(drop=True)
			
			print(df)
			df.to_csv('./df.csv')

			#df = pd.DataFrame(stat_tables)
			#print(df)
			#df = pd.concat(stat_tables, axis=1, sort=False)
			#print(df)

			#print(type(stat_tables))
			#print(type(stat_tables[0]))
			#df = stat_tables[0].join(stat_tables[1], how='left')
			#print(df)

			#player_stats = pd.DataFrame
			#player_stats = [player_stats.join(st) for st in stat_tables]
			#df = pd.merge(stat_tables[0], stat_tables[1])
			#print(df)

			#for stat_table in player_stats_sel.css('table[data-index] td.player-name::text'):
			#	print((stat_table))

			#for stat_table in player_stats_sel

			#ps_loader = ItemLoader(item=PlayerStats(), response=response)
			#ps_loader.add_value('match_id', match['match_id'])

			#ps_loader = ps_loader.nested_css(f"dv.match-centre-stats-page-team.{home_or_away}.full-player-stats")




	def team_page_parse(self,response):
		"""	
			Call function to parse a team page.
			Example url parsed: https://www.rugbypass.com/{tournament}/teams/{team}
		"""
		print(f"		    Parsing team page {response.url}")#
		
		# Return if team page redirected (team page doesn't exist any more)
		if response.url.split('/')[-1] is '':
			print(f"		       Team page {response.meta['url']} doesn't exist, returning")
			return

		if "We're sorry," in response.css("h1.center::text").get():
			print("		       No content in page, returning")
			return



		
