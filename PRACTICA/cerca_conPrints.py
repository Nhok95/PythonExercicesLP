#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import math
import webbrowser
import argparse as AP
from ast import literal_eval
import urllib.request as URL
import xml.etree.ElementTree as ET


class PuntI:
    def __init__(self, nom, adr, cont, desc, lat, lon):
        self.nom = nom
        self.adr = adr
        self.cont = cont
        self.desc = desc
        self.lat = lat
        self.lon = lon
    def __eq__(self, another):
        return self.lat == another.lat and self.lon == another.lon
    def __ne__(self, another):
        return not self == another
    def __hash__(self):
        return hash((self.nom, self.adr,
                    self.cont, self.desc,
                    self.lat, self.lon))

class Station:
    def __init__(self, idb, adr, status, slots, bikes, lat, lon):
        self.idb = idb
        self.adr = adr
        self.status = status
        self.slots = int(slots)
        self.bikes = int(bikes)
        self.lat = lat
        self.lon = lon
    def valid(self):
        return self.status == 'OPN'
    def __eq__(self, another):
        return (self.lat == another.lat and
                self.lon == another.lon and
                self.idb == another.idb
                )
    def __ne__(self, another):
        return not self == another
    def __gt__(self,another):
        return self.slots < another.slots


def ini_parser():
    parser = AP.ArgumentParser()

    parser.add_argument('--key', help ='key help')
    parser.add_argument('--lan', dest = 'language', nargs = '?',
                        const = 'cat', help ='lan help')
    global args
    args = parser.parse_args()


def lang_option():
    if args.language == 'es':
        lang = 'http://www.bcn.cat/tercerlloc/pits_opendata_es.xml'
    elif args.language == 'en':
        lang = 'http://www.bcn.cat/tercerlloc/pits_opendata_en.xml'
    elif args.language == 'fr':
        lang = 'http://www.bcn.cat/tercerlloc/pits_opendata_fr.xml'
    else:
        lang = 'http://www.bcn.cat/tercerlloc/pits_opendata.xml'
    return lang


def key_expr():
    if args.key:
        k = literal_eval(args.key)
    return k


def getXML(url):
    xml = URL.urlopen(url)
    tree = ET.fromstring(xml.read())
    xml.close
    return tree


def eval_string(k, xml, only):
    punts = []
    print ()
    for row in xml.iter("row"):
        t = False
        for child in row:
            #name
            if child.tag == 'name':
                name = child.text
                if (child.text.lower().find(k.lower()) > -1 and not t
                    and (only == 'name' or only == "")):
                    t = True
            #location
            if child.tag == 'address':
                adr = child.text
                if (child.text.lower().find(k.lower()) > -1 and not t
                    and (only == 'location' or only == "")):
                    t = True
            if child.tag == 'addresses' and not t:
                for ch2 in child[0]:
                    if ch2.tag == 'district':
                        if (ch2.text.lower().find(k.lower()) > -1
                            and (only == 'location' or only == "")):
                            t = True
                    if ch2.tag == 'barri':
                        if (ch2.text.lower().find(k.lower()) > -1
                            and (only == 'location' or only == "")):
                            t = True
            ##
            if child.tag == 'gmapy':
                y = child.text
            if child.tag == 'gmapx':
                x = child.text
            if child.tag == 'content':
                cont = child.text
                if cont.lower().find(k.lower()) > -1 and only == 'content':
                    t = True
            if child.tag == 'custom_fields':
                for ch2 in child:
                    if ch2.tag == 'descripcio-curta-pics':
                        desc = ch2.text
            if child.tag == 'wt' and t:
                print("name: ", name)
                punts.append(PuntI(name, adr, cont, desc, x, y))

    return punts


def eval_key(k,xml,only):
    punts = []
    if isinstance(k,list):
        print ("es un or")
        print (k)
        for subk in k:
            aux = eval_key(subk, xml, only)
            punts = punts + aux

    elif isinstance(k,tuple):
        print ("es un and")
        print (k)
        for subk in k:
            aux = eval_key(subk, xml, only)
            if len(punts) == 0:
                punts = aux
            else:
                aux2 = []
                for punt in aux:
                    if punt in punts:
                        aux2.append(punt)
                punts = aux2

    elif isinstance (k,dict):
        print ("dic")
        print (k)
        for subk in k:
            print (subk, k[subk])
            aux = eval_key(k[subk], xml, subk)
            if len(punts) == 0:
                punts = aux
                print ("length punts0:", len(punts))
            else:
                aux2 = []
                print("Comprobem else")
                for punt in aux:
                    print ("name punt:", punt.nom)
                    if punt in punts:
                        print ("-->name punt inclos:",punt.nom)
                        aux2.append(punt)
                punts = aux2
                print("length punts:", len(punts))

    else:
        punts = eval_string(k, xml, only)
        print ("length", len(punts))

    punts = list(set(punts))
    return punts


def get_bicis(xml):
    bicis = []
    for station in xml.iter('station'):
        for child in station:
            if child.tag == 'id':
                idb = child.text
            if child.tag == 'lat':
                lat = child.text
            if child.tag == 'long':
                lon = child.text
            if child.tag == 'street':
                adr = child.text
            elif child.tag == 'streetNumber':
                if child.text != None:
                    adr = adr + ' ' + child.text
            if child.tag == 'status':
                status = child.text
            if child.tag == 'slots':
                slots = child.text
            if child.tag == 'bikes':
                bikes = child.text
        bicis.append(Station(idb, adr, status, slots, bikes, lat, lon))
    return bicis


def deg2rad(deg):
    return deg*math.pi/180.0


def get_dist(lat1, lon1, lat2, lon2):
    R = 6371000.0   # radi terra en m
    lat = deg2rad(float(lat2)-float(lat1))
    lon = deg2rad(float(lon2)-float(lon1))
    sinLt = math.sin(lat/2)*math.sin(lat/2)
    sinLg = math.sin(lon/2)*math.sin(lon/2)
    cos1 = math.cos(deg2rad(float(lat1)))
    cos2 = math.cos(deg2rad(float(lat2)))
    a = sinLt + cos1*cos2*sinLg
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R*c    # distance


def near_stations_slots(punt,bicis):
    latP = punt.lat
    lonP = punt.lon
    slot_sort = sorted(bicis)
    st_dist = [ [get_dist(latP, lonP, s.lat, s.lon), s] for s in slot_sort]
    return (list(filter(lambda x: x[0] <= 500, st_dist)))


def near_stations_bikes(punt,bicis):
    latP = punt.lat
    lonP = punt.lon
    slot_sort2 = sorted(bicis, key=lambda b: b.bikes, reverse=True)
    st_dist2 = [ [get_dist(latP, lonP, s.lat, s.lon), s] for s in slot_sort2]
    return (list(filter(lambda x: x[0] <= 500, st_dist2)))


def HTML_init(f):
    code = """<!DOCTYPE html>
    <html>
        <head>
            <title>Practica Python </title>
            <meta charset="UTF-8" />
            <style>
                table { border-top:3px;border-bottom:3px }
                td { font-size:14px; padding:10px }
            </style>
        </head>
        <body>
            <table border="1" width="100%">
                <tr style="background-color:#0000ff">
                    <th rowspan="2" style="font-size:18px">Nom</th>
                    <th rowspan="2" style="font-size:18px">Adreça</th>
                    <th rowspan="2" style="font-size:18px">Descripció</th>
                    <th width ="25%" colspan="3" style="font-size:18px">
                        Aparcaments disponibles
                    </th>
                    <th width ="25%" colspan="3" style="font-size:18px">
                        Bicicletes disponibles
                    </th>
                </tr>
                <tr style="background-color:#0000ff">
                    <th>Adreça</th>
                    <th>Distancia(m)</th>
                    <th>Llocs</th>
                    <th>Adreça</th>
                    <th>Distancia(m)</th>
                    <th>Bicis</th>
                </tr>
                """
    f.write(code)


def HTML_end(f):
    code = """
            </table>
        </body>
    </html>"""
    f.write(code)

def write_HTML(punts,bicis):
    file_name = 'output.html'
    f = open(file_name, 'w')
    HTML_init(f)
    if len(punts) == 1:
        stations = near_stations_slots(punts[0], bicis)
        stations2 = near_stations_bikes(punts[0], bicis)
        st = ["","","","",""]
        dist = ["","","","",""]
        val = ["","","","",""]
        st2 = ["","","","",""]
        dist2 = ["","","","",""]
        val2 = ["","","","",""]
        for s in range(min(len(stations),5)):
            st[s] = stations[s][1].adr
            dist[s] = float('%.3f'%stations[s][0])
            val[s] = stations[s][1].slots
        for s2 in range(min(len(stations2),5)):
            st2[s2] = stations2[s2][1].adr
            dist2[s2] = float('%.3f'%stations2[s2][0])
            val2[s2] = stations2[s2][1].bikes
        code = """
                    <tr style="background-color:#d6eaf8">
                        <td rowspan="5">%s</td>
                        <td rowspan="5">%s</td>
                        <td rowspan="5">%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <tr style="background-color:#d6eaf8">
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                        </tr>
                        <tr style="background-color:#d6eaf8">
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                        </tr>
                        <tr style="background-color:#d6eaf8">
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                        </tr>
                        <tr style="background-color:#d6eaf8">
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                        </tr>
                    </tr>
        """ % (punts[0].nom, punts[0].adr, punts[0].cont,
            st[0], dist[0], val[0], st2[0], dist2[0], val2[0],
            st[1], dist[1], val[1], st2[1], dist2[1], val2[1],
            st[2], dist[2], val[2], st2[2], dist2[2], val2[2],
            st[3], dist[3], val[3], st2[3], dist2[3], val2[3],
            st[4], dist[4], val[4], st2[4], dist2[4], val2[4])
        f.write(code)
    else:
        for punt in punts:
            stations = near_stations_slots(punt, bicis)
            stations2 = near_stations_bikes(punt, bicis)

            st = ["","","","",""]
            dist = ["","","","",""]
            val = ["","","","",""]
            st2 = ["","","","",""]
            dist2 = ["","","","",""]
            val2 = ["","","","",""]
            for s in range(min(len(stations),5)):
                st[s] = stations[s][1].adr
                dist[s] = float('%.3f'%stations[s][0])
                val[s] = stations[s][1].slots
            for s2 in range(min(len(stations2),5)):
                st2[s2] = stations2[s2][1].adr
                dist2[s2] = float('%.3f'%stations2[s2][0])
                val2[s2] = stations2[s2][1].bikes
            code = """
                        <tr style="background-color:#d6eaf8">
                            <td rowspan="5">%s</td>
                            <td rowspan="5">%s</td>
                            <td rowspan="5">%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <tr style="background-color:#d6eaf8">
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                            </tr>
                            <tr style="background-color:#d6eaf8">
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                            </tr>
                            <tr style="background-color:#d6eaf8">
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                            </tr>
                            <tr style="background-color:#d6eaf8">
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                            </tr>
                        </tr>
            """ % (punt.nom, punt.adr, punt.desc,
                st[0], dist[0], val[0], st2[0], dist2[0], val2[0],
                st[1], dist[1], val[1], st2[1], dist2[1], val2[1],
                st[2], dist[2], val[2], st2[2], dist2[2], val2[2],
                st[3], dist[3], val[3], st2[3], dist2[3], val2[3],
                st[4], dist[4], val[4], st2[4], dist2[4], val2[4])
            f.write(code)
    HTML_end(f)
    f.close()
    webbrowser.open(file_name)


def Main():
    ini_parser()
    lang_url = lang_option()

    k = key_expr()

    xml_interes = getXML(lang_url)
    # busquem punts d'interes
    punts = eval_key(k,xml_interes,"")

    xml = getXML('http://wservice.viabicing.cat/v1/getstations.php?v=1')
    # guardem informació necesaria de les estacións bicing
    bicis = get_bicis(xml)

    write_HTML(punts,bicis)
    print("archiu .html generat")


if __name__ == '__main__':
    Main()
