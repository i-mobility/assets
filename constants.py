
class TransportProvider:
  def __init__(self, id):
    self.id = id

  def localized_name(self):
    match self.id:
      case "route_start":
        return _('transportation_label.route_start')
      case "route_end":
        return _('transportation_label.route_end')
      case "region_bike_sharing":
        return _('transportation_label.region_bike_sharing')
      case "region_escooters":
        return _('transportation_label.region_escooters')
      case "region_car_rental":
        return _('transportation_label.region_car_rental')
      case "postbus_station":
        return _('transportation_label.postbus_station')
      case "train":
        return _('transportation_label.train')
      case "long_distance_bus":
        return _('transportation_label.long_distance_bus')
      case "city_train":
        return _('transportation_label.city_train')
      case "s_bahn":
        return _('transportation_label.s_bahn')
      case "sbahn":
        return _('transportation_label.sbahn')
      case "metro":
        return _('transportation_label.metro')
      case "metro_u1":
        return _('transportation_label.metro')
      case "metro_u2":
        return _('transportation_label.metro')
      case "metro_u3":
        return _('transportation_label.metro')
      case "metro_u4":
        return _('transportation_label.metro')
      case "metro_u6":
        return _('transportation_label.metro')
      case "ship":
        return _('transportation_label.ship')
      case "tram":
        return _('transportation_label.tram')
      case "innsbruck_1":
        return _('transportation_label.tram')
      case "innsbruck_2":
        return _('transportation_label.tram')
      case "innsbruck_3":
        return _('transportation_label.tram')
      case "innsbruck_5":
        return _('transportation_label.tram')
      case "innsbruck_6":
        return _('transportation_label.tram')
      case "innsbruck_STB":
        return _('transportation_label.tram')
      case "tram_vienna":
        return _('transportation_label.tram_vienna')
      case "bus":
        return _('transportation_label.bus')
      case "salzburg_obus_1":
        return _('transportation_label.trolleybus')
      case "salzburg_obus_2":
        return _('transportation_label.trolleybus')
      case "salzburg_obus_3":
        return _('transportation_label.trolleybus')
      case "salzburg_obus_4":
        return _('transportation_label.trolleybus')
      case "salzburg_obus_5":
        return _('transportation_label.trolleybus')
      case "salzburg_obus_6":
        return _('transportation_label.trolleybus')
      case "salzburg_obus_7":
        return _('transportation_label.trolleybus')
      case "salzburg_obus_8":
        return _('transportation_label.trolleybus')
      case "salzburg_obus_9":
        return _('transportation_label.trolleybus')
      case "salzburg_obus_10":
        return _('transportation_label.trolleybus')
      case "salzburg_obus_12":
        return _('transportation_label.trolleybus')
      case "salzburg_obus_14":
        return _('transportation_label.trolleybus')
      case "innsbruck_A":
        return _('transportation_label.bus')
      case "innsbruck_C":
        return _('transportation_label.bus')
      case "innsbruck_F":
        return _('transportation_label.bus')
      case "innsbruck_J":
        return _('transportation_label.bus')
      case "innsbruck_K":
        return _('transportation_label.bus')
      case "innsbruck_M":
        return _('transportation_label.bus')
      case "innsbruck_R":
        return _('transportation_label.bus')
      case "innsbruck_T":
        return _('transportation_label.bus')
      case "innsbruck_W":
        return _('transportation_label.bus')
      case "innsbruck_NX":
        return _('transportation_label.bus')
      case "innsbruck_5XX":
        return _('transportation_label.bus')
      case "city_bus":
        return _('transportation_label.bus')
      case "express_bus":
        return _('transportation_label.bus')
      case "regional_bus":
        return _('transportation_label.bus')
      case "dialaride":
        return _('transportation_label.dialaride')
      case "innsbruck_HBB":
        return _('transportation_label.dialaride')
      case "sev":
        return _('transportation_label.sev')
      case "cable_car":
        return _('transportation_label.cable_car')
      case "cartrain":
        return _('transportation_label.cartrain')
      case "oebb":
        return _('transportation_label.oebb')
      case "westbahn":
        return _('transportation_label.westbahn')
      case "cat":
        return _('transportation_label.cat')
      case "regiojet":
        return _('transportation_label.regiojet')
      case "val":
        return _('transportation_label.val')
      case "digibus":
        return _('transportation_label.digibus')
      case "walk":
        return _('transportation_label.walk')
      case "car":
        return _('transportation_label.car')
      case "bike":
        return _('transportation_label.bike')
      case "taxi":
        return _('transportation_label.taxi')
      case "taxi_40100":
        return _('transportation_label.taxi_40100')
      case "citybike":
        return _('transportation_label.citybike')
      case "green4rent":
        return _('transportation_label.green4rent')
      case "region_nextbike":
        return _('transportation_label.nextbike')
      case "nextbike":
        return _('transportation_label.nextbike')
      case "nextbike_burgenland":
        return _('transportation_label.nextbike_burgenland')
      case "nextbike_niederoesterreich":
        return _('transportation_label.nextbike_niederoesterreich')
      case "city_bike_linz":
        return _('transportation_label.city_bike_linz')
      case "wienmobil_rad":
        return _('transportation_label.wienmobil_rad')
      case "stadtrad_innsbruck":
        return _('transportation_label.stadtrad_innsbruck')
      case "regiorad_tirol":
        return _('transportation_label.regiorad_tirol')
      case "oebb_bike":
        return _('transportation_label.oebb_bike')
      case "ladestellen":
        return _('transportation_label.ladestellen')
      case "ride_and_charge":
        return _('transportation_label.ride_and_charge')
      case "taxi_rank":
        return _('transportation_label.taxi_rank')
      case "radbox":
        return _('transportation_label.vvt_radbox')
      case "vvt_radbox":
        return _('transportation_label.vvt_radbox')
      case "uber":
        return _('transportation_label.uber')
      case "parken_at":
        return _('transportation_label.parken_at')
      case "blablacar":
        return _('transportation_label.blablacar')
      case "park_and_ride":
        return _('transportation_label.park_and_ride')
      case "getaround":
        return _('transportation_label.getaround')
      case "family_of_power":
        return _('transportation_label.family_of_power')
      case "postbus":
        return _('transportation_label.postbus')
      case "oebb_transfer":
        return _('transportation_label.oebb_transfer')
      case "sharenow":
        return _('transportation_label.sharenow')
      case "free2move":
        return _('transportation_label.free2move')
      case "caruso":
        return _('transportation_label.caruso')
      case "rail_and_drive":
        return _('transportation_label.rail_and_drive')
      case "gourban":
        return _('transportation_label.gourban')
      case "kiwi":
        return _('transportation_label.kiwi')
      case "lime":
        return _('transportation_label.lime')
      case "dott":
        return _('transportation_label.dott')
      case "dott_bike":
        return _('transportation_label.dott')
      case "bird":
        return _('transportation_label.bird')
      case "bird_parking":
        return _('transportation_label.bird')
      case "dott_parking":
        return _('transportation_label.dott')
      case "lime_parking":
        return _('transportation_label.lime')
      case "link":
        return _('transportation_label.link')

class TransportProviders:
  ROUTE_START = TransportProvider("route_start")
  ROUTE_END = TransportProvider("route_end")
  REGION_BIKE_SHARING = TransportProvider("region_bike_sharing")
  REGION_ESCOOTERS = TransportProvider("region_escooters")
  REGION_CAR_RENTAL = TransportProvider("region_car_rental")
  POSTBUS_STATION = TransportProvider("postbus_station")
  TRAIN = TransportProvider("train")
  LONG_DISTANCE_BUS = TransportProvider("long_distance_bus")
  CITY_TRAIN = TransportProvider("city_train")
  S_BAHN = TransportProvider("s_bahn")
  SBAHN = TransportProvider("sbahn")
  METRO = TransportProvider("metro")
  METRO_U1 = TransportProvider("metro_u1")
  METRO_U2 = TransportProvider("metro_u2")
  METRO_U3 = TransportProvider("metro_u3")
  METRO_U4 = TransportProvider("metro_u4")
  METRO_U6 = TransportProvider("metro_u6")
  SHIP = TransportProvider("ship")
  TRAM = TransportProvider("tram")
  INNSBRUCK_1 = TransportProvider("innsbruck_1")
  INNSBRUCK_2 = TransportProvider("innsbruck_2")
  INNSBRUCK_3 = TransportProvider("innsbruck_3")
  INNSBRUCK_5 = TransportProvider("innsbruck_5")
  INNSBRUCK_6 = TransportProvider("innsbruck_6")
  INNSBRUCK_STB = TransportProvider("innsbruck_STB")
  TRAM_VIENNA = TransportProvider("tram_vienna")
  BUS = TransportProvider("bus")
  SALZBURG_OBUS_1 = TransportProvider("salzburg_obus_1")
  SALZBURG_OBUS_2 = TransportProvider("salzburg_obus_2")
  SALZBURG_OBUS_3 = TransportProvider("salzburg_obus_3")
  SALZBURG_OBUS_4 = TransportProvider("salzburg_obus_4")
  SALZBURG_OBUS_5 = TransportProvider("salzburg_obus_5")
  SALZBURG_OBUS_6 = TransportProvider("salzburg_obus_6")
  SALZBURG_OBUS_7 = TransportProvider("salzburg_obus_7")
  SALZBURG_OBUS_8 = TransportProvider("salzburg_obus_8")
  SALZBURG_OBUS_9 = TransportProvider("salzburg_obus_9")
  SALZBURG_OBUS_10 = TransportProvider("salzburg_obus_10")
  SALZBURG_OBUS_12 = TransportProvider("salzburg_obus_12")
  SALZBURG_OBUS_14 = TransportProvider("salzburg_obus_14")
  INNSBRUCK_A = TransportProvider("innsbruck_A")
  INNSBRUCK_C = TransportProvider("innsbruck_C")
  INNSBRUCK_F = TransportProvider("innsbruck_F")
  INNSBRUCK_J = TransportProvider("innsbruck_J")
  INNSBRUCK_K = TransportProvider("innsbruck_K")
  INNSBRUCK_M = TransportProvider("innsbruck_M")
  INNSBRUCK_R = TransportProvider("innsbruck_R")
  INNSBRUCK_T = TransportProvider("innsbruck_T")
  INNSBRUCK_W = TransportProvider("innsbruck_W")
  INNSBRUCK_NX = TransportProvider("innsbruck_NX")
  INNSBRUCK_5XX = TransportProvider("innsbruck_5XX")
  CITY_BUS = TransportProvider("city_bus")
  EXPRESS_BUS = TransportProvider("express_bus")
  REGIONAL_BUS = TransportProvider("regional_bus")
  DIALARIDE = TransportProvider("dialaride")
  INNSBRUCK_HBB = TransportProvider("innsbruck_HBB")
  SEV = TransportProvider("sev")
  CABLE_CAR = TransportProvider("cable_car")
  CARTRAIN = TransportProvider("cartrain")
  OEBB = TransportProvider("oebb")
  WESTBAHN = TransportProvider("westbahn")
  CAT = TransportProvider("cat")
  REGIOJET = TransportProvider("regiojet")
  VAL = TransportProvider("val")
  DIGIBUS = TransportProvider("digibus")
  WALK = TransportProvider("walk")
  CAR = TransportProvider("car")
  BIKE = TransportProvider("bike")
  TAXI = TransportProvider("taxi")
  TAXI_40100 = TransportProvider("taxi_40100")
  CITYBIKE = TransportProvider("citybike")
  GREEN4RENT = TransportProvider("green4rent")
  REGION_NEXTBIKE = TransportProvider("region_nextbike")
  NEXTBIKE = TransportProvider("nextbike")
  NEXTBIKE_BURGENLAND = TransportProvider("nextbike_burgenland")
  NEXTBIKE_NIEDEROESTERREICH = TransportProvider("nextbike_niederoesterreich")
  CITY_BIKE_LINZ = TransportProvider("city_bike_linz")
  WIENMOBIL_RAD = TransportProvider("wienmobil_rad")
  STADTRAD_INNSBRUCK = TransportProvider("stadtrad_innsbruck")
  REGIORAD_TIROL = TransportProvider("regiorad_tirol")
  OEBB_BIKE = TransportProvider("oebb_bike")
  LADESTELLEN = TransportProvider("ladestellen")
  RIDE_AND_CHARGE = TransportProvider("ride_and_charge")
  TAXI_RANK = TransportProvider("taxi_rank")
  RADBOX = TransportProvider("radbox")
  VVT_RADBOX = TransportProvider("vvt_radbox")
  UBER = TransportProvider("uber")
  PARKEN_AT = TransportProvider("parken_at")
  BLABLACAR = TransportProvider("blablacar")
  PARK_AND_RIDE = TransportProvider("park_and_ride")
  GETAROUND = TransportProvider("getaround")
  FAMILY_OF_POWER = TransportProvider("family_of_power")
  POSTBUS = TransportProvider("postbus")
  OEBB_TRANSFER = TransportProvider("oebb_transfer")
  SHARENOW = TransportProvider("sharenow")
  FREE2MOVE = TransportProvider("free2move")
  CARUSO = TransportProvider("caruso")
  RAIL_AND_DRIVE = TransportProvider("rail_and_drive")
  GOURBAN = TransportProvider("gourban")
  KIWI = TransportProvider("kiwi")
  LIME = TransportProvider("lime")
  DOTT = TransportProvider("dott")
  DOTT_BIKE = TransportProvider("dott_bike")
  BIRD = TransportProvider("bird")
  BIRD_PARKING = TransportProvider("bird_parking")
  DOTT_PARKING = TransportProvider("dott_parking")
  LIME_PARKING = TransportProvider("lime_parking")
  LINK = TransportProvider("link")
