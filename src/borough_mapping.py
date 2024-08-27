'''
Constants for mapping the borough cd/id to the location the testing was performed
# mappings, take the average of aqi of locations in the list
# https://data.cityofnewyork.us/City-Government/Community-Districts/yfnk-k7r4
# https://a816-dohbesp.nyc.gov/IndicatorPublic/neighborhood-reports/downtown_heights_slope/
# https://communityprofiles.planning.nyc.gov/brooklyn/2
'''

# Respective average Min and Max values anually/seasonally.
NYC_ANNUAL_MIN_AQI   = 7.38
NYC_ANNUAL_MAX_AQI   = 27.45
NYC_SEASONAL_MIN_AQI = 10.1 
NYC_SEASONAL_MAX_AQI = 30.83

# ["Time Period"] Column
# Used for seasonal scroll bar & calculating seasonal averages
SEASONAL_AQI_AVERAGE = ( 
    'Winter 2008-09', 'Summer 2009',
    'Winter 2009-10', 'Summer 2010',
    'Winter 2010-11', 'Summer 2011',
    'Winter 2011-12', 'Summer 2012',
    'Winter 2012-13', 'Summer 2013',
    'Winter 2013-14', 'Summer 2014',
    'Winter 2014-15', 'Summer 2015',
    'Winter 2015-16', 'Summer 2016',
    'Winter 2016-17', 'Summer 2017',
    'Winter 2017-18', 'Summer 2018',
    'Winter 2018-19', 'Summer 2019', 
    'Winter 2019-20', 'Summer 2020', 
    'Winter 2020-21', 'Summer 2021',
    'Winter 2021-22', 'Summer 2022' 
)

# ["Time Period"] Column
# Used for yearly scroll bar & calculating annual averages
ANNUAL_AQI_AVERAGE = (
    'Annual Average 2009', 'Annual Average 2010', 'Annual Average 2011',
    'Annual Average 2012', 'Annual Average 2013', 'Annual Average 2014',
    'Annual Average 2015', 'Annual Average 2016', 'Annual Average 2017',
    'Annual Average 2018', 'Annual Average 2019', 'Annual Average 2020',
    'Annual Average 2021', 'Annual Average 2022'
)

# The first instance is the value of the "boro_cd" key in the data/nyc_community_districts.geojson
# The remainder values of the tuple are the districts of column "Geo Place Name" in data/cleaned_aqi_data.csv
BORO_CDS = (
    ('101', 'Financial District (CD1)'),
    ('102', 'Greenwich Village and Soho (CD2)', 'Greenwich Village - SoHo'),
    ('103', 'Lower East Side and Chinatown (CD3)'),
    ('104', 'Chelsea - Clinton', 'Clinton and Chelsea (CD4)', 'Chelsea-Village'),
    ('105', 'Union Square - Lower East Side', 'Midtown (CD5)', 'Union Square-Lower Manhattan'),
    ('106', 'Gramercy Park - Murray Hill', 'Stuyvesant Town and Turtle Bay (CD6)', 'Upper East Side-Gramercy'),
    ('107', 'Upper West Side', 'Upper West Side (CD7)'),
    ('108', 'Upper East Side (CD8)', 'Upper East Side', 'Upper East Side-Gramercy'),
    ('109', 'Central Harlem - Morningside Heights', 'Morningside Heights and Hamilton Heights (CD9)'),
    ('110', 'Central Harlem (CD10)', 'Central Harlem - Morningside Heights'),
    ('111', 'East Harlem', 'East Harlem (CD11)'),
    ('112', 'Washington Heights', 'Washington Heights and Inwood (CD12)'),
    ('201', 'Hunts Point - Mott Haven', 'Mott Haven and Melrose (CD1)'),
    ('202', 'Hunts Point and Longwood (CD2)', 'Hunts Point - Mott Haven'),
    ('203', 'Morrisania and Crotona (CD3)', 'High Bridge - Morrisania', 'Crotona -Tremont'),
    ('204', 'Highbridge and Concourse (CD4)', 'High Bridge - Morrisania'),
    ('205', 'Fordham - Bronx Pk'),
    ('206', 'Belmont and East Tremont (CD6)'),
    ('207', 'Kingsbridge Heights and Bedford (CD7)', 'Fordham and University Heights (CD5)'),
    ('208', 'Riverdale and Fieldston (CD8)', 'Kingsbridge - Riverdale'),
    ('209', 'Parkchester and Soundview (CD9)'),
    ('210', 'Pelham - Throgs Neck', 'Throgs Neck and Co-op City (CD10)'),
    ('211', 'Morris Park and Bronxdale (CD11)'),
    ('212', 'Northeast Bronx', 'Williamsbridge and Baychester (CD12)'),
    ('301', 'Greenpoint', 'Greenpoint and Williamsburg (CD1)', 'Williamsburg - Bushwick'),
    ('302', 'Downtown - Heights - Slope', 'Fort Greene and Brooklyn Heights (CD2)'),
    ('303', 'Bedford Stuyvesant (CD3)'),
    ('304', 'Bushwick (CD4)', 'Williamsburg - Bushwick'),
    ('305', 'East New York', 'East New York and Starrett City (CD5)'),
    ('306', 'Downtown - Heights - Slope', 'Park Slope and Carroll Gardens (CD6)'),
    ('307', 'Sunset Park (CD7)', 'Sunset Park'),
    ('308', 'Bedford Stuyvesant - Crown Heights', 'Crown Heights and Prospect Heights (CD8)'),
    ('309', 'South Crown Heights and Lefferts Gardens (CD9)'),
    ('310', 'Bensonhurst - Bay Ridge', 'Bay Ridge and Dyker Heights (CD10)'),
    ('311', 'Bensonhurst - Bay Ridge', 'Bensonhurst (CD11)'),
    ('312', 'Borough Park'),
    ('313', 'Coney Island (CD13)'),
    ('314', 'East Flatbush - Flatbush'),
    ('315', 'Coney Island - Sheepshead Bay', 'Sheepshead Bay (CD15)'),
    ('316', 'Brownsville (CD16)'),
    ('317', 'East Flatbush - Flatbush', 'East Flatbush (CD17)'),
    ('318', 'Canarsie - Flatlands', 'Flatlands and Canarsie (CD18)'),
    ('401', 'Long Island City - Astoria', 'Long Island City and Astoria (CD1)'),
    ('402', 'Woodside and Sunnyside (CD2)'),
    ('403', 'Jackson Heights (CD3)'),
    ('404', 'Elmhurst and Corona (CD4)'),
    ('405', 'Ridgewood - Forest Hills', 'Ridgewood and Maspeth (CD5)'),
    ('406', 'Rego Park and Forest Hills (CD6)', 'Ridgewood - Forest Hills'),
    ('407', 'Flushing and Whitestone (CD7)', 'Flushing - Clearview'),
    ('408', 'Fresh Meadows', 'Hillcrest and Fresh Meadows (CD8)', 'Bayside Little Neck-Fresh Meadows', 'Jamaica'),
    ('409', 'Kew Gardens and Woodhaven (CD9)'),
    ('410', 'South Ozone Park and Howard Beach (CD10)'),
    ('411', 'Bayside - Little Neck', 'Bayside Little Neck-Fresh Meadows', 'Bayside and Little Neck (CD11)'),
    ('412', 'Jamaica', 'Jamaica and Hollis (CD12)'),
    ('413','Southeast Queens'),
    ('414', 'Rockaways', 'Rockaway and Broad Channel (CD14)'),
    ('484', 'Rockaway and Broad Channel (CD14)'),
    ('501', 'Port Richmond', 'St. George and Stapleton (CD1)', 'Northern SI', 'Stapleton - St. George'),
    ('502', 'Willowbrook', 'South Beach and Willowbrook (CD2)', 'South Beach - Tottenville'),
    ('503', 'Southern SI', 'Tottenville and Great Kills (CD3)', 'South Beach - Tottenville'),
)

# Legend for standard AQI colors
TRUE_LEGEND_HTML = '''
    {% macro html(this, kwargs) %}

    <div style="
        position: fixed; 
        bottom: 20px; 
        left: 50%; 
        transform: translateX(-50%);
        width: 90%;  /* Increase width */
        height: 60px;  /* Increase height */
        background: linear-gradient(to right, rgb(0, 228, 0), rgb(255, 255, 0), rgb(255, 126, 0), rgb(255, 0, 0), rgb(143, 63, 151), rgb(126, 0, 35)); 
        border:2px solid black; 
        z-index:1000; 
        font-size:12px;
        line-height: 1.2em;  /* Adjust line height */
        color: black;  /* Set font color to black */
        text-align: center;
        padding: 5px 10px;  /* Add padding */
        box-sizing: border-box;
    ">

        <span style="float:left; width: 12%; text-align: center;"><strong>0-50</strong><br>(Good)</span>
        <span style="float:left; width: 12%; text-align: center;"><strong>51-100</strong><br>(Moderate)</span>
        <span style="float:left; width: 18%; text-align: center;"><strong>101-150</strong><br>(Unhealthy for Sensitive Groups)</span>
        <span style="float:left; width: 14%; text-align: center;"><strong>151-200</strong><br>(Unhealthy)</span>
        <span style="float:left; width: 14%; text-align: center;"><strong>201-300</strong><br>(Very Unhealthy)</span>
        <span style="float:right; width: 14%; text-align: center;"><strong>301-500</strong><br>(Hazardous)</span>
    </div>

    {% endmacro %}
    '''



# Custom legend for visualizing and defining NYC's min and max AQI values/colors
NYC_LEGEND_HTML = '''
    {% macro html(this, kwargs) %}

    <div style="
        position: fixed; 
        bottom: 20px; 
        left: 50%; 
        transform: translateX(-50%);
        width: 90%;  /* Increase width */
        height: 60px;  /* Increase height to accommodate the text */
        background: linear-gradient(to right, rgb(0, 228, 0), rgb(255, 255, 0), rgb(255, 126, 0), rgb(255, 0, 0), rgb(143, 63, 151), rgb(126, 0, 35)); 
        border: 2px solid black; 
        z-index: 1000; 
        font-size: 12px;
        line-height: 1.2em;  /* Adjust line height */
        color: black;  /* Set font color to black */
        text-align: center;
        padding: 5px 10px;  /* Add padding */
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: center;
    ">

        <!-- Adjusted labels for the AQI range -->
        <div style="display: flex; justify-content: space-between; width: 100%;">
            <span style="text-align: center;"><strong>7.38</strong><br>(NYC Min AQI)</span>
            <span style="text-align: center;"><strong>15</strong></span>
            <span style="text-align: center;"><strong>20</strong></span>
            <span style="text-align: center;"><strong>25</strong></span>
            <span style="text-align: center;"><strong>30.83</strong><br>(NYC Max AQI)</span>
        </div>

        <!-- Centered message indicating the AQI values are good -->
        <div style="
            margin-top: 5px;
            text-align: center;
            font-weight: bold;
            width: 100%;
        ">
             Air Quality Index Values in This Range (0-50) Are Good 
        </div>
    </div>

    {% endmacro %}
    '''













