import streamlit as st
from streamlit_option_menu import option_menu
import os
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import plotly.express as px
import requests
import json
import webbrowser


st.set_page_config(page_title="PHONEPE DATA VISUALIZATION", page_icon=":money_with_wings:")

# Apply custom CSS
st.markdown("""<style>.main { max-width: 1200px; }</style>""", unsafe_allow_html=True)

def fetch_data(table_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Prasanna@23",
        database="PhonePe_Project1"
    )
    
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in cursor.description]
    
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)
    mydb.commit()
    
    return df


df11 = fetch_data("AI")
df12 = fetch_data("AT")
df13 = fetch_data("AU")
df14 = fetch_data("MI")
df15 = fetch_data("MT")
df16 = fetch_data("MU")
df17 = fetch_data("TI")
df18 = fetch_data("TT")
df19 = fetch_data("TU")

#1 AI Transaction Year wise
def Year_Sort(df,year):
    dfy = df[df["Year"] == year]
    dfy.reset_index(drop=True, inplace=True)
    dfyg = dfy.groupby("State")[["Transaction_count", "Transaction_amount"]].sum()
    dfyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_TA= px.bar(dfyg, x="State", y="Transaction_amount", title=f"{year} Transaction Amount",width=600, height= 650, color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_TA)
    with col2:
        fig_TC= px.bar(dfyg, x="State", y="Transaction_count", title=f"{year} Transaction Count",width=600, height= 650, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_TC)

    col1,col2= st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        State_Name=[]
        for feature in data1["features"]:
            State_Name.append(feature["properties"]['ST_NM'])
        State_Name.sort()

        AIM1= px.choropleth(dfyg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                        color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                        range_color= (dfyg["Transaction_amount"].min(),dfyg["Transaction_amount"].max()),
                                        hover_name= "State",title = f"{year} TRANSACTION AMOUNT",
                                        fitbounds= "locations",width =600, height= 600)
        
        AIM1.update_geos(visible =False) #Remove unwanted lines
        st.plotly_chart(AIM1)

    with col2:
        AIM2= px.choropleth(dfyg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                        color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                        range_color= (dfyg["Transaction_count"].min(),dfyg["Transaction_count"].max()),
                                        hover_name= "State",title = f"{year} Transaction Count",
                                        fitbounds= "locations",width =600, height= 600)
        
        AIM2.update_geos(visible =False) #Remove unwanted lines
        st.plotly_chart(AIM2)
    return dfy

#2 AI Transaction Quater wise
def Quarter_Sort(df,Quater):
    dfy = df[df["Quater"] == Quater]
    dfy.reset_index(drop=True, inplace=True)
    dfyg = dfy.groupby("State")[["Transaction_count", "Transaction_amount"]].sum()
    dfyg.reset_index(inplace=True)

    col1,col2= st.columns(2)

    with col1:
        fig_TA= px.bar(dfyg, x="State", y="Transaction_amount", 
                             title=f"{dfy['Year'].min()}Year{Quater}Quater TRANSACTION AMOUNT",width= 600, height=650,
                             color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_TA)


    with col2:
        fig_TC= px.bar(dfyg, x="State", y="Transaction_count", 
                       title=f"{dfy['Year'].min()}Year{Quater}Quater TRANSACTION COUNT",width= 600, height=650,
                       color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_TC)


    col1,col2= st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        State_Name=[]
        for feature in data1["features"]:
            State_Name.append(feature["properties"]['ST_NM'])
        State_Name.sort()
        
        AIMQ1= px.choropleth(dfyg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                    color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                    range_color= (dfyg["Transaction_amount"].min(),dfyg["Transaction_amount"].max()),
                                    hover_name= "State",title = f"{dfy['Year'].min()}Year{Quater}Quater TRANSACTION AMOUNT",
                                    fitbounds= "locations",width =600, height= 600)
    
        AIMQ1.update_geos(visible =False) #Remove unwanted lines
        st.plotly_chart(AIMQ1)


    with col2:
        AIMQ2= px.choropleth(dfyg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                    color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                    range_color= (dfyg["Transaction_count"].min(),dfyg["Transaction_count"].max()),
                                    hover_name= "State",title = f"{dfy['Year'].min()}Year{Quater}Quater TRANSACTION COUNT",
                                    fitbounds= "locations",width =600, height= 600)
    
        AIMQ2.update_geos(visible =False) #Remove unwanted lines
        st.plotly_chart(AIMQ2)
    
    return dfy

#3 AT State Year wise
def AT_TT(df,state):
    dfy = df[df["State"] == state]
    dfy.reset_index(drop=True, inplace=True)

    dfttg = dfy.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    dfttg.reset_index(inplace=True)

    col1,col2= st.columns(2)
    with col1:
        fig_TA=px.pie(data_frame=dfttg, names="Transaction_type", values="Transaction_amount",width=600,
                    title=f"{state.upper()} Transaction_amount", hole=0.5)
        st.plotly_chart(fig_TA)
    
    with col2:
        fig_TC=px.pie(data_frame=dfttg, names="Transaction_type", values="Transaction_count",width=600,
                    title=f"{state.upper()} Transaction_count", hole=0.5)
        st.plotly_chart(fig_TC)

#4 AU Year Wise
def AU_Y(df,year):
    AUY3 = df[df["Year"] ==year].reset_index(drop=True)
    AUYG = pd.DataFrame(AUY3.groupby("Brands")["Transaction_count"].sum())
    AUYG.reset_index(inplace=True)

    fig_AUY= px.bar(AUYG, x="Brands",y= "Transaction_count", title=f"{year}BRANDS AND TRANSACTION COUNT",
                        width=1000,color_discrete_sequence=px.colors.sequential.Rainbow,hover_name="Brands")
    st.plotly_chart(fig_AUY)
    return AUY3

#5 AU Quarter Wise
def AU_Q(df,Quater):
    AUQ3 = df[df["Quater"] ==Quater].reset_index(drop=True)
    AUQG = pd.DataFrame(AUQ3.groupby("Brands")["Transaction_count"].sum())
    AUQG.reset_index(inplace=True)

    fig_AUQ= px.bar(AUQG, x="Brands",y= "Transaction_count", title=f"{Quater}QUARTER BRANDS AND TRANSACTION COUNT",
                            width=1000,color_discrete_sequence=px.colors.sequential.Rainbow, hover_name="Brands")
    st.plotly_chart(fig_AUQ)
    return AUQ3

#6 AU State Wise
def AU_S(df,State):
    AU_S=df[df["State"] == State]
    AU_S.reset_index(drop=True,inplace=True)

    fig_AUS= px.line(AU_S, x="Brands",y= "Transaction_count", hover_data="Percentage",
                    title=f"{State} BRANDS,PERCENTAGE AND TRANSACTION COUNT",markers=True,
                                width=1000,color_discrete_sequence=px.colors.sequential.Rainbow, hover_name="Brands")
    st.plotly_chart(fig_AUS)

#7 MI Distrits wise
def MI_D(df,state):
    dfy = df[df["State"] == state]
    dfy.reset_index(drop=True, inplace=True)

    dfdg = dfy.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    dfdg.reset_index(inplace=True)
    col1,col2= st.columns(2)
    with col1:
        fig_MID=px.bar(data_frame=dfdg,x="Transaction_amount",y="Districts",orientation="h",height=650,
                title=f"{state.upper()} Transaction_amount",color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_MID)
    with col2:
        fig_MID1=px.bar(data_frame=dfdg,x="Transaction_count",y="Districts",orientation="h",height=650,
                    title=f"{state.upper()} Transaction_count",color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_MID1)

#8 MU Year Wise
def MU_Y(df,Year):
    dfy = df[df["Year"] == Year]
    dfy.reset_index(drop=True, inplace=True)
    dfyg = pd.DataFrame(dfy.groupby("State")[["RegisteredUsers", "AppOpens"]].sum())
    dfyg.reset_index(inplace=True)
    fig_MUY= px.line(dfyg, x="State",y=["RegisteredUsers","AppOpens"], 
                        title=f"{Year} RegisteredUsers and AppOpens",markers=True,
                                    width=1000,height=600, color_discrete_sequence=px.colors.sequential.Rainbow, hover_name="State")
    st.plotly_chart(fig_MUY)
    return dfy

#9 MU Quater Wise
def MU_Q(df,Quater):
    muq = df[df["Quater"] == Quater]
    muq.reset_index(drop=True, inplace=True)
    dfqg = pd.DataFrame(muq.groupby("State")[["RegisteredUsers", "AppOpens"]].sum())
    dfqg.reset_index(inplace=True)
    fig_MUQ= px.line(dfqg, x="State",y=["RegisteredUsers","AppOpens"], 
                        title=f"{df['Year'].min()} Year {Quater}Quarter RegisteredUsers and AppOpens",markers=True,
                                    width=1000,height=600, color_discrete_sequence=px.colors.sequential.Rainbow, hover_name="State")
    st.plotly_chart(fig_MUQ)
    return muq

#10 MU State Wise
def MU_S(df, state):
    mu_s= df[df["State"] ==state].reset_index(drop=True)
   
    col1,col2= st.columns(2)
    with col1:
        fig_MUS1=px.bar(data_frame=mu_s,x="RegisteredUsers",y="Districts",orientation="h",height=650,
                        title=f"{state} REGISTERED USERS",color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_MUS1)
    with col2:

        fig_MUS2=px.bar(data_frame=mu_s,x="AppOpens",y="Districts",orientation="h",height=650,
                        title=f"{state} APP OPENS",color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_MUS2)

#11 TI District Wise
def TID(df, state):
    TID= df[df["State"] == state]
    TID.reset_index(drop=True, inplace=True)
    TIDG =TID.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    TIDG.reset_index(inplace=True)
     
    fig_TID1=px.bar(data_frame=TIDG,x="Transaction_count",y="Districts",orientation="h",height=650,hover_data="Districts",
                        title="Transaction Count",color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_TID1)

    fig_TID2=px.bar(data_frame=TIDG,x="Transaction_amount",y="Districts",orientation="h",height=650,hover_data="Districts",
                        title="Transaction Amount",color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_TID2)


#12 TU
def TUSQ(df, year):
    dfy = df[df["Year"] == year]
    dfy.reset_index(drop=True, inplace=True)
    dfsq = pd.DataFrame(dfy.groupby(["State", "Quater"])["RegisteredUsers"].sum().reset_index())

    fig_TUSQ = px.bar(data_frame=dfsq, x="State", y="RegisteredUsers", color="Quater", height=650, 
                    facet_col="Quater", 
                    title=f"{year} Registered Users", 
                    color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_TUSQ)
    return dfy

#13 TU Quater wise
def TU_Q(df,state):
    dfy = df[df["State"] == state]
    dfy.reset_index(drop=True, inplace=True)

    fig_TUSQ = px.bar(data_frame=dfy, x="Quater", y="RegisteredUsers", color="Quater", height=650, 
                        facet_col="Districts", hover_data="Districts",
                        title="Registered Users", 
                        color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_TUSQ)

def execute_query(query):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Prasanna@23",
        database="PhonePe_Project1"
    )
    cursor = mydb.cursor()

    try:
        print(f"Executing Query: {query}")
        cursor.execute(query)
        result = cursor.fetchall()
        print(f"Query Result: {result}")
        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        mydb.close()

def question_1():
    query = '''WITH RankedData AS (SELECT State, Year, Transaction_count, ROW_NUMBER() OVER (PARTITION BY Year ORDER BY 
                Transaction_count DESC) AS RowNum FROM AI) SELECT State, Year, MAX(Transaction_count) 
                OVER (PARTITION BY Year) AS Max_Transaction_count_Per_Year FROM RankedData WHERE RowNum = 1 ORDER BY Transaction_count
                ASC, RowNum;'''
    result = execute_query(query)
    st.write(pd.DataFrame(result, columns=["State","Year","Transaction Count"]))

def question_2():
    query = '''SELECT Year, Quater, AVG(Transaction_amount) AS AvgTransactionAmount FROM AI WHERE 
                Transaction_type = 'Insurance' GROUP BY Year, Quater ORDER BY Year DESC, AvgTransactionAmount DESC LIMIT 12;'''
    result = execute_query(query)
    st.write(pd.DataFrame(result, columns=["Year","Quater", "Avg Transaction Amount"]))

def question_3():
    query = '''SELECT Districts, SUM(Transaction_count) AS TotalTransactionCount
               FROM MT GROUP BY Districts ORDER BY TotalTransactionCount DESC LIMIT 10;'''
    result = execute_query(query)
    st.write(pd.DataFrame(result, columns=["Districts", "Total Transaction Count"]))

def question_4():
    query = '''SELECT State, Quater, SUM(Transaction_count) AS TotalTransactionCount, SUM(Transaction_amount) AS TotalTransactionAmount
            FROM TI GROUP BY State, Quater ORDER BY TotalTransactionCount DESC;'''
    result = execute_query(query)
    st.write(pd.DataFrame(result, columns=["State","Quater","Transaction_count","Transaction_amount"]))

def question_5():
    query = '''SELECT Districts, SUM(RegisteredUsers) AS TotalRegisteredUsers, SUM(AppOpens) AS TotalAppOpens FROM 
    MU GROUP BY Districts ORDER BY TotalRegisteredUsers DESC;'''
    result = execute_query(query)
    st.write(pd.DataFrame(result, columns=["Districts", "Total Registered Users", "Total App Opens"]))

def question_6():
    query = '''SELECT State, SUM(Transaction_amount) AS Total_Transaction_Amount FROM MI GROUP BY State ORDER BY Total_Transaction_Amount DESC;
'''
    result = execute_query(query)
    st.write(pd.DataFrame(result, columns=["State", "Total Premium Amount"]))

def question_7():
    query = '''WITH RankedTransactions AS (SELECT State, Year, Quater, Districts, SUM(Transaction_amount) AS Total_Transaction_amount, ROW_NUMBER() OVER (PARTITION BY Year ORDER BY SUM(Transaction_amount) DESC) AS RowNum FROM TT GROUP BY State, Year, Quater, Districts) SELECT State, Year, Quater, Districts, Total_Transaction_amount FROM RankedTransactions WHERE RowNum <= 10 ORDER BY Year, Total_Transaction_amount ASC;'''
    result = execute_query(query)
    st.write(pd.DataFrame(result, columns=["State","Year","Quater","Districts","Transaction Amount"]))

def question_8():
    query = '''SELECT State, Brands, SUM(Transaction_count) AS Total_Transaction_count FROM AU GROUP BY State, Brands ORDER BY Total_Transaction_count DESC LIMIT 10;'''
    result = execute_query(query)
    st.write(pd.DataFrame(result, columns=["State", "Brand","Total Transaction_Count"]))

def question_9():
    query = '''SELECT Year, SUM(Transaction_amount) AS TotalTransactionAmount 
               FROM AI WHERE Transaction_type = 'Insurance' GROUP BY Year;'''
    result = execute_query(query)
    st.write(pd.DataFrame(result, columns=["Year", "Total Transaction Amount"]))

def question_10():
    query = '''SELECT State, SUM(AppOpens) AS TotalAppOpens FROM MU GROUP BY State ORDER BY TotalAppOpens DESC LIMIT 10;'''
    result = execute_query(query)
    st.write(pd.DataFrame(result, columns=["State","TotalAppOpens"]))

def handle_top_charts():
    st.header("Top Charts Analysis")

    question_options = {
        "1.The maximum transaction count and the corresponding state for each year from Aggregated Insurance Table": question_1,
        "2.The average transaction amount for Quarter Wise Aggregated Insurance Table": question_2,
        "3.Top 10 districts with the highest transaction count from Map transaction table": question_3,
        "4.The total transaction count and total transaction amount for each state and quarter from the 'TI' table": question_4,
        "5.Number of registered users and app opens in each district": question_5,
        "6.Top 10 total transaction amount for each state from the MI table ": question_6,
        "7.Least 10 State that have lowest Transaction Amount": question_7,
        "8.The top 10 brand-state combinations with the highest total transaction counts in the 'AU' table": question_8,
        "9.Total transaction amount per year for 'Insurance' transactions": question_9,
        "10.The top 10 states with the highest total 'AppOpens' in the 'MU' table": question_10,
    }

    selected_question = st.selectbox(
        'Please Select Your Question',
        list(question_options.keys())
    )

    try:
        if st.button("Submit"):
            question_options[selected_question]()
    except mysql.connector.Error as err:
        print(f"Error: {err}")



#Streamlit part
def display_home():
    st.markdown(
        """
        <style>
            .big-font {
                font-size: 24px;
                font-weight: bold;
                color: #2f4f4f;
            }
            .info-box {
                background-color: #f0f8ff;
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
            }
            .marquee {
                color: #4682b4;
                font-size: 18px;
                white-space: nowrap;
                overflow: hidden;
                border: 1px solid #b0c4de;
                padding: 10px;
                border-radius: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    scrolling_text = "<h1 style='color:red; font-style: italic; font-weight: bold;'>Welcome to PhonePe Pulse - Your Financial Insights Hub</marquee></h1>"
    st.markdown(scrolling_text, unsafe_allow_html=True)

    st.title("PhonePe Pulse Project")
    st.markdown("<p class='big-font'>Unlocking Financial Insights with PhonePe Pulse</p>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='info-box'>
            <p><strong>About PhonePe:</strong></p>
            <p>PhonePe is a leading digital payments platform in India. It provides a secure and convenient
            way for users to make payments, transfer money, and engage in various financial transactions.</p>
            <p><strong>Uses of PhonePe:</strong></p>
            <ul>
                <li>Mobile Recharge and Bill Payments</li>
                <li>Money Transfers</li>
                <li>Online Shopping</li>
                <li>UPI Payments</li>
            </ul>
            <p>Explore PhonePe Pulse to understand the dynamics of these transactions and improve user experiences.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        PhonePe Pulse is a revolutionary project designed to offer comprehensive insights into financial transactions and trends.
        Explore the data to gain valuable information about user behaviors, transaction patterns, and much more.
    """)


def open_phonepe():
    phonepe_url_scheme = 'https://www.phonepe.com/'

    try:
        webbrowser.open(phonepe_url_scheme)
    except Exception as e:
        print(f"Error: {e}")
        print("Unable to open the PhonePe app. Please check if the app supports deep linking.")



with st.sidebar:
    select = option_menu("Main Menu", ["Home", "Data Exploration", "Top Charts","Website"])

if select == "Home":
    image_url1 = "data:image/jpeg;base64,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"
    st.sidebar.image(image_url1, caption='PhonePe- Easy Pay', use_column_width=True)
    display_home()   

elif select == "Data Exploration":
    image_url1 = "data:image/jpeg;base64,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"
    st.sidebar.image(image_url1, caption='PhonePe- Easy Pay', use_column_width=True)
    
    tab1, tab2, tab3= st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method = st.radio("**Select the Analysis Method**",["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("**Select the Year**", df11["Year"].min(), df11["Year"].max(), df11["Year"].min())
                available_quarters = pd.Series(df11[df11["Year"] == years]["Quater"].unique())


            with col2:
                quarters = st.slider("**Select the Quarter**",min_value=available_quarters.min(),max_value=available_quarters.max(),value=available_quarters.min())
            analysis_type = st.radio("Choose Analysis Type", ["Year Analysis", "Quarter Analysis"])
            if st.button("Show Analysis"):
                AIY1 = Year_Sort(df11, years)
                if analysis_type == "Year Analysis":
                    st.write("Performing Year Analysis")
                elif analysis_type == "Quarter Analysis":
                    Quarter_Sort(AIY1, quarters)
                    st.write("Performing Quarter Analysis")
        

        elif method == "Transaction Analysis":
            col = st.columns(3)  # Create a single row with 3 columns

            with col[0]:
                years = st.slider("**Select the Year**", df12["Year"].min(), df12["Year"].max(), df12["Year"].min())
                available_states = pd.Series(df12[df12["Year"] == years]["State"].unique())

            with col[1]:
                states = st.selectbox("**Select the State**", available_states)

            AIY1 = Year_Sort(df12, years)  # Move AIY1 definition outside the if condition

            with col[2]:
                quarters = st.slider(
                    "**Select the Quarter**",
                    min_value=pd.Series(AIY1["Quater"]).min(),
                    max_value=pd.Series(AIY1["Quater"]).max(),
                    value=pd.Series(AIY1["Quater"]).min()
                )

            analysis_type = st.radio("Choose Analysis Type", ["Year Analysis", "Quarter Analysis"])

            if analysis_type == "Year Analysis":
                AT_TT(AIY1, states)
            if analysis_type == "Quarter Analysis":
                # Move the ATQ2 definition outside the button check
                ATQ2 = Quarter_Sort(AIY1, quarters)
                states_quarter = st.selectbox("**Select the State_Quarter**", ATQ2["State"].unique())

                if st.button("Show Analysis"):
                    AT_TT(ATQ2, states_quarter)


        elif method == "User Analysis":
            col = st.columns(3) 

            with col[0]:
                years = st.slider("**Select the Year**", df13["Year"].min(), df13["Year"].max(), df13["Year"].min())

            with col[1]:
                quarters = st.slider(
                    "**Select the Quarter**",
                    min(df13["Quater"]),
                    max(df13["Quater"]),
                    min(df13["Quater"])
                )

            with col[2]:
                states = st.selectbox("**Select the State**", df13["State"].unique())

            if st.button("Show Analysis"):
                AUY3 = AU_Y(df13, years)
                AUQ3 = AU_Q(AUY3, quarters)
                AU_S(AUQ3, states)


    with tab2:
        method_map = st.radio("**Select the Analysis Method(MAP)**",["Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"])

        if method_map == "Map Insurance Analysis":
            col = st.columns(4)  # Create a single row with 4 columns

            with col[0]:
                years = st.slider("**Select the Year**", df14["Year"].min(), df14["Year"].max(), df14["Year"].min(), key="year_slider")

            with col[1]:
                quarters = st.slider(
                    "**Select the Quarter**",
                    min(df14["Quater"]),
                    max(df14["Quater"]),
                    min(df14["Quater"]),
                    key="quarter_slider"
                )

            with col[2]:
                states = st.selectbox("**Select the State**", df14["State"].unique(), key="state_selectbox")

            show_analysis_button_key = "show_analysis_button"  # Unique key for the button
            if st.button("Show Analysis", key=show_analysis_button_key):
                MIY1 = Year_Sort(df14, years)
                MIQ2 = Quarter_Sort(MIY1, quarters)
                MI_D(MIQ2, states)
            

        elif method_map == "Map Transaction Analysis":
            col1, col2, col3 = st.columns(3)

            with col1:
                years = st.slider("**Select the Year**", df15["Year"].min(), df15["Year"].max(), df15["Year"].min())

            with col2:
                quarters = st.slider("**Select the Quarter**", df15["Quater"].min(), df15["Quater"].max(), df15["Quater"].min())

            with col3:
                state_m3 = st.selectbox("Select the State", df15["State"].unique())

            analysis_button_key = "analysis_button"  # Unique key for the button
            if st.button("Show Analysis", key=analysis_button_key):
                MTY2 = Year_Sort(df15, years)
                MTQ2 = Quarter_Sort(MTY2, quarters)
                MI_D(MTQ2, state_m3)


        
        elif method_map == "Map User Analysis":
            col1,col2,col3= st.columns(3)
            with col1:
                years= st.slider("**Select the Year**", df16["Year"].min(), df16["Year"].max(),df16["Year"].min())

            with col2:
                quarters = st.slider("**Select the Quarter2**", min(df16["Quater"]), max(df16["Quater"]), min(df16["Quater"]))
            
            with col3:
                States=st.selectbox("**Select the STATE2**",df16["State"].unique())
            

            analysis_button_key = "analysis_button"  # Unique key for the button
            if st.button("Show Analysis", key=analysis_button_key):
                MUY= MU_Y(df16, years)
                MUQ2=MU_Q(MUY,quarters)
                MU_S(MUQ2,States)



    with tab3:
        method_top = st.radio("**Select the Analysis Method(TOP)**",["Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"])

        if method_top == "Top Insurance Analysis":
            col1,col2,col3= st.columns(3)
            with col1:
                years= st.slider("**Select the Year-TI**", df17["Year"].min(), df17["Year"].max(),df17["Year"].min())

            with col2:
                State = st.selectbox("**Select the State-TI**", df17["Districts"].unique())

            with col3:

                quarters = st.slider( "**Select the Quarter2**", int(df17["Quater"].min()),int(df17["Quater"].max()),
                int(df17["Quater"].min()),key="unique_key_for_quarter_slider")
                
            analysis_button_key = "analysis_button1"  # Unique key for the button
            if st.button("Show Analysis", key=analysis_button_key):
                TIY=Year_Sort(df17,years)
                TIQ=Quarter_Sort(TIY,quarters)



        
        elif method_top == "Top Transaction Analysis":

            col1,col2= st.columns(2)
            with col1:
                years_t2= st.slider("**Select the Year_tt**", df18["Year"].min(), df18["Year"].max(),df18["Year"].min())
 
            
            with col2:
                quarters_t2= st.slider("**Select the Quarter_tt**", df18["Quater"].min(), df18["Quater"].max(),df18["Quater"].min())

            
            analysis_button_key = "analysis_button2"

            if st.button("Show Analysis", key=analysis_button_key):
                TTY= Year_Sort(df18,years_t2)
                TTQ= Quarter_Sort(TTY, quarters_t2)


        elif method_top == "Top User Analysis":
            col1,col2,col3= st.columns(3)
            with col1:
                years_t3= st.selectbox("**Select the Year_tu**", df19["Year"].unique())
            with col2:
                quarters_t2= st.slider("**Select the Quarter_tu**", df19["Quater"].min(), df19["Quater"].max(),df19["Quater"].min())

            with col3:
                state_t3= st.selectbox("**Select the State_tu**", df19["State"].unique())

            analysis_button_key = "analysis_button3"

            if st.button("Show Analysis", key=analysis_button_key):
                 TUYQ= TUSQ(df19,years_t3)
                 TU_Q(TUYQ,state_t3)
            


elif select == "Top Charts":
    image_url1 = "data:image/jpeg;base64,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"
    st.sidebar.image(image_url1, caption='PhonePe- Easy Pay', use_column_width=True)
    handle_top_charts()


elif select == "Download PhonePe":
    image_url1 = "data:image/jpeg;base64,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"
    st.sidebar.image(image_url1, caption='PhonePe- Easy Pay', use_column_width=True)
    open_phonepe()    




            



