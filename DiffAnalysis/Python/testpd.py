import pandas as pd

if __name__ == "__main__":
    df3 =pd.DataFrame(data=[['A','B','C','1'],['E','G','L','1']])
    df4 =pd.DataFrame(data=[['A','B','C','1'],['E','G','L','1']])
    m = pd.DataFrame(data=[[1,2],[3,4],[5,6]])
    print(m[1])
    if df3.equals(df4):
        print("yes")
    p = df3.iloc[:,-1]
    print(len(df3.iloc[:,-1] == '1'))

    df4 =pd.DataFrame(data=[['A','B','C','D'],['E','G','L','O']])
    print(pd.merge(df3,df4,how='outer'))
    d = df4[0].value_counts()
    print(d.index)

