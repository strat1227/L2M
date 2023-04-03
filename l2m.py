import pandas as pd
pd.set_option('display.max_columns', 50)

def get_ref_dict():

    def compare(row):
        if row['away_score'] > row['home_score']:
            return 'away'
        elif row['home_score'] > row['away_score']:
            return 'home'

    #url='https://atlhawksfanatic.github.io/L2M/1-tidy/L2M/L2M.csv'
    df=pd.read_csv('l2m_table.csv', low_memory=False)
    df = df.drop(df[df['bkref_id'].isin(['201504100UTA', '201504150CHI', '201601170DEN'])].index)
    df['winner'] = df.apply(compare, axis=1)
    df['disadvantaged_side_mode'] = df.groupby('bkref_id')['disadvantaged_side'].transform(lambda x: x.mode().iloc[0])
    df['loser_matches_disadvantaged_side_mode'] = df['winner'] != df['disadvantaged_side_mode']
    incor_calls=(df.loc[df['decision'].isin(['INC','IC'])])

    ref_dict = {}
    seen_games = set()

    for index, row in incor_calls.iterrows():
        if row['bkref_id'] in seen_games:
            continue
        else:
            seen_games.add(row['bkref_id'])

        bad_break = row['loser_matches_disadvantaged_side_mode'] == True

        for ref in [row["ref_1"], row["ref_2"], row["ref_3"]]:
            if ref in ref_dict:
                ref_dict[ref]['total_games'] += 1
                ref_dict[ref]['bad_breaks'] += 1 if bad_break else 0
            else:
                ref_dict[ref] = {'bad_breaks': 1 if bad_break else 0, 'total_games': 1}

    
    for ref in ref_dict:
        ref_dict[ref]['bad_percent']= round((ref_dict[ref]['bad_breaks']/ref_dict[ref]['total_games'])*100,2)
        

    return ref_dict


def main():
    get_ref_dict()

if __name__ == '__main__':
    main()