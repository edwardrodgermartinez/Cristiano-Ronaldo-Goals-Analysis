import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
import datetime
import pandas as pd

cr7_rm_transformed = pd.read_csv('data/cr7_rm_transformed.csv', encoding='latin1')

def visualisation (cr7_rm_transformed):
    
    sns.set_context("poster")
    sns.set(rc={"figure.figsize": (12.,6.)})
    sns.set_style("whitegrid")
    
    #1
    goals_by_star_sign = cr7_rm_transformed['Star Sign'].value_counts().reset_index()
    goals_by_star_sign.columns = ['Star Sign', 'Total Goals']
    goals_by_star_sign = goals_by_star_sign.sort_values(by='Total Goals', ascending=False)
    
    sns.countplot(data=cr7_rm_transformed, x='Star Sign', color='#CDB8FF', order=goals_by_star_sign['Star Sign'])
    plt.xlabel("Star Sign")
    plt.title("1. Total goals scored by Cristiano Ronaldo in each star sign during 9 seasons at Real Madrid")
    plt.ylabel("Goals")
    plt.xticks(rotation=45)
    plt.savefig("images/figure1.png")
    plt.show()
    
    #2
    sns.countplot(data=cr7_rm_transformed, x='Star Sign', hue='Venue', palette='pastel', order=goals_by_star_sign['Star Sign'])
    plt.xlabel("Star Sign")
    plt.title("2. Total goals scored in each star sign, home and away")
    plt.ylabel("Goals")
    plt.xticks(rotation=45)
    plt.legend(title='Home / Away', loc='upper right')
    plt.savefig("images/figure2.png")
    plt.show()
    
    #3
    condition_cl = (cr7_rm_transformed['Competition'] == 'UEFA Champions League') & (cr7_rm_transformed['Matchday'].isin(['last 16', 'Quarter-Finals', 'Semi-Finals', 'Final']))
    condition_copa = (cr7_rm_transformed['Competition'] == 'Copa del Rey') & (cr7_rm_transformed['Matchday'].isin(['Semi-Finals', 'Final']))
    condition_clasico_derbi = cr7_rm_transformed['Opponent'].isin(['Atletico de Madrid', 'FC Barcelona'])
    condition_big_games = (condition_cl | condition_copa | condition_clasico_derbi)
    cr7_rm_big_games = cr7_rm_transformed[condition_big_games]
    goals_by_star_sign_2 = cr7_rm_big_games['Star Sign'].value_counts().reset_index()
    goals_by_star_sign_2.columns = ['Star Sign', 'Total Goals']
    goals_by_star_sign_2 = goals_by_star_sign_2.sort_values(by='Total Goals', ascending=False)
    sns.countplot(data=cr7_rm_big_games, x='Star Sign', color='#FFD700', order=goals_by_star_sign_2['Star Sign'])
    plt.xlabel("Star Sign")
    plt.title("3. Total goals scored in important matches by C.Ronaldo in each star sign (Clásicos, Derbis, Champions League knockouts, Copa del Rey Semis or Final)")
    plt.ylabel("Goals")
    plt.xticks(rotation=45)
    plt.savefig("images/figure3.png")
    plt.show()
    
    #4
    goals_by_distance = cr7_rm_transformed['Distance from Aquarius'].value_counts().reset_index()
    goals_by_distance.columns = ['Distance from Aquarius', 'Total Goals']
    goals_by_distance = goals_by_distance.sort_values(by='Distance from Aquarius', ascending=True)
    goals_by_distance_df = pd.DataFrame(goals_by_distance)
    goals_by_distance_df['Weighted_total_goals'] = ['44', '45', '55.5', '49', '29.5', '22.5', '5']
    
    goals_by_distance_big_games = cr7_rm_big_games['Distance from Aquarius'].value_counts().reset_index()
    goals_by_distance_big_games.columns = ['Distance from Aquarius', 'Total Goals']
    goals_by_distance_big_games = goals_by_distance_big_games.sort_values(by='Distance from Aquarius', ascending=True)
    goals_by_distance_big_games_df = pd.DataFrame(goals_by_distance_big_games)
    goals_by_distance_big_games_df['Weighted_total_goals'] = ['8', '10', '15.5', '8.5', '2.5', '1', '3']
    
    condition_home = cr7_rm_transformed['Venue'] == 'H'
    cr7_rm_home = cr7_rm_transformed[condition_home]
    goals_by_distance_home = cr7_rm_home['Distance from Aquarius'].value_counts().reset_index()
    goals_by_distance_home.columns = ['Distance from Aquarius', 'Total Goals']
    goals_by_distance_home = goals_by_distance_home.sort_values(by='Distance from Aquarius', ascending=True)
    goals_by_distance_home_df = pd.DataFrame(goals_by_distance_home)
    goals_by_distance_home_df['Weighted_total_goals'] = ['32', '27.5', '30.5', '21.5', '15.5', '13', '2']
    
    custom_labels = ['All Matches', 'Important Matches', 'All Home Matches']

    Weighted_total_goals_as_float1 = goals_by_distance_df['Weighted_total_goals'].astype(float)
    Weighted_total_goals_as_float2 = goals_by_distance_big_games_df['Weighted_total_goals'].astype(float)
    Weighted_total_goals_as_float3 = goals_by_distance_home_df['Weighted_total_goals'].astype(float)

    sns.lineplot(data=goals_by_distance_df, x='Distance from Aquarius', y=Weighted_total_goals_as_float1, label=custom_labels[0], color='#CDB8FF', marker='o')
    sns.lineplot(data=goals_by_distance_big_games_df, x='Distance from Aquarius', y=Weighted_total_goals_as_float2, label=custom_labels[1], color='#FFD700', marker='s')
    sns.lineplot(data = goals_by_distance_home_df, x='Distance from Aquarius', y=Weighted_total_goals_as_float3, label=custom_labels[2], color='#FF6B6B', marker='h')
    plt.xlabel("Distance from Aquarius (in star signs/months)")
    plt.ylabel("Total Goals (Weighted)")
    plt.title("4. Total Goals vs. Distance from Aquarius")
    plt.savefig("images/figure4.png")
    plt.show()