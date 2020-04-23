import mysql.connector
import pymysql

def connect():
    global mydb, mycursor
    print("Connecting...")
    mydb = pymysql.connect(
        host="192.168.1.3",
        user="root",
        database="brew_project"
    )
    mycursor = mydb.cursor()


def disconnect():
    print("Disconnecting...")
    mycursor.close()
    mydb.close()


def insert_query(query):
    mycursor.execute(query)
    mydb.commit()


def load_style(filename):
    with open(filename) as f:
        style = [line.split(',') for line in f]
        for i, x in enumerate(style):
            style = [x[0].strip(), x[1].strip(), x[2].strip(), x[3].strip(), x[4].strip(), x[5].strip(), x[6].strip(),
                     x[7].strip(), x[8].strip(), x[9].strip(), x[10].strip(), x[11].strip()]
            insert_query('INSERT INTO style(style_name, style_category, style_bjcp, style_min_ibu, style_max_ibu, '
                         'style_min_abv, style_max_abv, style_min_fg, style_max_fg, style_min_co2_vol, '
                         'style_max_co2_vol, style_lovibond)'
                         'VALUES("{0[0]}", "{0[1]}", "{0[2]}", {0[3]}, {0[4]}, {0[5]}, {0[6]}, {0[7]}, {0[8]}, {0[9]}, '
                         '{0[10]}, {0[11]})'.format(style))
            print('Added: Name: {0[0]}, Category: {0[1]}, BJCP: {0[2]}, IBU: {0[3]} - {0[4]}, ABV: {0[5]} - {0[6]}, '
                  'Final Gravity: {0[7]} - {0[8]}, CO2 Volume: {0[9]} - {0[10]}, Lovibond: {0[11]}'.format(style))


def load_malt(filename):
    with open(filename) as f:
        malt = [line.split(',') for line in f]
        for i, x in enumerate(malt):
            malt = [x[0].strip(), x[1].strip(), x[2].strip(), x[3].strip(), x[4].strip(), x[5].strip()]
            insert_query('INSERT INTO malt(malt_name, malt_origin, malt_category, malt_type, malt_lovibond, '
                         'malt_ppg) '
                         'VALUES("{0[0]}", "{0[1]}", "{0[2]}", "{0[3]}", {0[4]}, {0[5]})'.format(malt))
            print('Added: Name: {0[0]}, Origin: {0[1]}, Category: {0[2]}, Type: {0[3]}, Lovibond: {0[4]}, '
                  'PPG: {0[5]}'.format(malt))


def load_hops(filename):
    with open(filename) as f:
        hops = [line.split(',') for line in f]
        for i, x in enumerate(hops):
            hop = [x[0].strip(), x[1].strip(), x[2].strip(), x[3].strip()]
            insert_query('INSERT INTO hops(hops_variety, hops_type, hops_aa, hops_use) '
                         'VALUES("{0[0]}", "{0[1]}", {0[2]}, "{0[3]}")'.format(hop))
            print('Added: Variety: {0[0]}, Type: {0[1]}, Average Alpha Acids: {0[2]}, Use: {0[3]}'.format(hop))


def load_yeast(filename):
    with open(filename) as f:
        yeasts = [line.split(',') for line in f]
        for i, x in enumerate(yeasts):

            yeast = [x[0].strip(), x[1].strip(), x[2].strip(), x[3].strip(), x[4].strip(), x[5].strip(), x[6].strip(),
                     x[7].strip()]
            insert_query('INSERT INTO yeast(yeast_strain, yeast_lab, yeast_code, yeast_type, yeast_floc, yeast_atten, '
                         'yeast_min_temp, yeast_max_temp)'
                         'VALUES("{0[0]}", "{0[1]}", "{0[2]}", "{0[3]}", "{0[4]}", {0[5]}, {0[6]}, {0[7]})'
                         .format(yeast))
            print('Added: Strain: {0[0]}, Lab: {0[1]}, Code: {0[2]}, Type: {0[3]}, Floccuation: {0[4]}, '
                  'Attenuation: {0[5]}, Min Tem: {0[6]}, Max Temp: {0[7]}'.format(yeast))


def load_images(filename):
    with open(filename) as f:
        images = [line.split(',') for line in f]
        for i, x in enumerate(images):
            image = [x[0].strip(), x[1].strip()]
            insert_query('INSERT INTO image(image_description, image_url) '
                         'VALUES("{0[0]}", "{0[1]}")'.format(image))
            print('Added: Description: {0[0]}, URL: {0[1]}'.format(image))


def load_all_data():
    connect()
    print('Loading all data...')
    load_style('csv/style.csv')
    load_malt('csv/malt.csv')
    load_hops('csv/hops.csv')
    load_yeast('csv/yeast.csv')
    load_images('csv/images.csv')
    print('...upload completed!')
    disconnect()


load_all_data()
