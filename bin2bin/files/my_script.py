import httpx
import json
import sqlite3

url = "https://www.njlottery.com/api/v1/instant-games/games/?size=1000&_=1726803357743"
response = httpx.get(url)

if response.status_code == 200:
    data = response.json()
    # Process the data as needed
    print(data)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('lottery_games.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            game_id INTEGER PRIMARY KEY,
            game_name TEXT,
            ticket_price REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prize_tiers (
            tier_id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER,
            tier_number INTEGER,
            prize_amount REAL,winning_tickets INTEGER,
            FOREIGN KEY (game_id) REFERENCES games (game_id)
        )
    ''')
     # Insert data into tables
    for game in data:
        game_id = game.get("gameId")
        game_name = game.get("gameName")
        ticket_price = game.get("ticketPrice") / 100.0
        prize_tiers = game.get("prizeTiers", [])
        
        cursor.execute('''
            INSERT OR REPLACE INTO games (game_id, game_name, ticket_price)
            VALUES (?, ?, ?)
        ''', (game_id, game_name, ticket_price))
        
        for tier in prize_tiers:
            tier_number = tier.get("tierNumber")
            prize_amount = tier.get("prizeAmount")
            winning_tickets = tier.get("winningTickets")
            
            cursor.execute('''
                            INSERT OR REPLACE INTO games (game_id, game_name, ticket_price)
            VALUES (?, ?, ?)
        ''', (game_id, game_name, ticket_price))
        
        for tier in prize_tiers:
            tier_number = tier.get("tierNumber")
            prize_amount = tier.get("prizeAmount")
            winning_tickets = tier.get("winningTickets")
            
            cursor.execute('''
                INSERT INTO prize_tiers (game_id, tier_number, prize_amount, winning_tickets)
                VALUES (?, ?, ?, ?)
            ''', (game_id, tier_number, prize_amount, winning_tickets))
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()
    