from ytmusicsme import YTMusic
import sys
import pandas as pd

def main():
    filename = sys.argv[1]

    file1 = open(filename, 'r')
    Lines = file1.readlines()
    
    yt = YTMusic()

    df_list = []
    for artistid in Lines:
        
        artists_stats_id = yt.get_stats_artistid(artistid.strip())
        print(artists_stats_id)
        df = yt.get_stats(artists_stats_id)
        df['src_artist_id'] = artistid.strip()
        df_list.append(df)

    df_final = pd.concat(df_list, ignore_index=True)
    df_final.to_excel('result.xlsx',index=False)

if __name__ == "__main__":
    main()