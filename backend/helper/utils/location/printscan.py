import logging, requests
import traceback
from django.conf import settings
from account.models import CodeConfirmation, User
from billing.models import Transaction
from helper.utils.email.send_mail import Email
from helper.utils.response.response_format import bad_request_response, success_response , internal_server_error_response
from identity.models.application import NationalIdentificationNumberApplication


usa_state_2_code = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}


locations_sample_response = [

    {
        "locationId": "abda8dfc-f421-ec11-981f-000d3a12914c",
        "name": "Accurate Notary & Fingerprinting",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Randallstown, MD",
        "description": None,
        "metaDescription": "Welcome to PrintScan in Randallstown, Maryland, your ultimate hub for efficient Live Scan and Fingerprinting services. Enjoy our swift, secure, and dependable fingerprinting procedures at PrintScan Randallstown today.",
        "notes": "Welcome to PrintScan in Randallstown, Maryland, your ultimate hub for efficient Live Scan and Fingerprinting services. Enjoy our swift, secure, and dependable fingerprinting procedures at PrintScan Randallstown today.",
        "address1": "9830 Liberty Road",
        "address2": None,
        "stateCountry": "MD",
        "city": "Randallstown",
        "postalCode": "21133",
        "county": "Baltimore",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -76.822038,
        "latitude": 39.381251,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-02-06T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-06T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-02-06T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-06T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-02-06T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-06T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-02-06T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-06T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-02-06T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-06T17:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-02-06T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-06T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    
    {
        "locationId": "4664a5ce-f422-ec11-981f-000d3a12914c",
        "name": "TruIdentity Fingerprint Services and More, LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Davie, FL",
        "description": None,
        "metaDescription": "Explore PrintScan in Davie, Florida, your trusted destination for advanced Live Scan and Fingerprinting services. Experience our quick, secure, and reliable fingerprinting solutions at PrintScan Davie today.",
        "notes": "Explore PrintScan in Davie, Florida, your trusted destination for advanced Live Scan and Fingerprinting services. Experience our quick, secure, and reliable fingerprinting solutions at PrintScan Davie today.",
        "address1": "4801 South University Drive",
        "address2": "Suite 209B",
        "stateCountry": "FL",
        "city": "Davie",
        "postalCode": "33328",
        "county": "Broward",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.253311,
        "latitude": 26.061215,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-02-13T11:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-13T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-05-18T11:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-18T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T11:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "bc864d8d-abfa-eb11-b563-000d3a12922c",
        "name": "Elite Firearms",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Myrtle Beach, SC",
        "description": "Inside Elite Firearms",
        "metaDescription": "Turn to PrintScan in Myrtle Beach, South Carolina, for exceptional Live Scan and Fingerprinting services. Experience our dedication to providing fast, secure, and reliable solutions that meet your specific needs.",
        "notes": "Turn to PrintScan in Myrtle Beach, South Carolina, for exceptional Live Scan and Fingerprinting services. Experience our dedication to providing fast, secure, and reliable solutions that meet your specific needs.",
        "address1": "3120 Waccamaw Blvd",
        "address2": "Unit A",
        "stateCountry": "SC",
        "city": "Myrtle Beach",
        "postalCode": "29579",
        "county": "Horry",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -78.925863,
        "latitude": 33.718082,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "ea9ea459-2a04-ec11-b563-000d3a12922c",
        "name": "Reed Security Training Academy, LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Bonita Springs, FL",
        "description": None,
        "metaDescription": "Looking for trusted Live Scan and Fingerprinting services in Bonita Springs, FL? PrintScan is your go-to solution for accurate and speedy results. Contact us today!",
        "notes": "Looking for trusted Live Scan and Fingerprinting services in Bonita Springs, FL? PrintScan is your go-to solution for accurate and speedy results. Contact us today!",
        "address1": "27499 Riverview Center Blvd",
        "address2": "Suite 110",
        "stateCountry": "FL",
        "city": "Bonita Springs",
        "postalCode": "34134",
        "county": "Collier",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.808068,
        "latitude": 26.341588,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T12:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T12:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T12:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T12:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T12:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "f851f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "The UPS Store 4287",
        "displayName": "PrintScan | UPS Store 4287 - SANTEE, CA",
        "description": None,
        "metaDescription": "Discover PrintScan in Santee, California, your trusted source for efficient Live Scan and Fingerprinting services. We offer high-quality, reliable solutions tailored to your needs.",
        "notes": "Discover PrintScan in Santee, California, your trusted source for efficient Live Scan and Fingerprinting services. We offer high-quality, reliable solutions tailored to your needs.",
        "address1": "9625 MISSION GORGE RD",
        "address2": "STE B2",
        "stateCountry": "CA",
        "city": "SANTEE",
        "postalCode": "92071",
        "county": "San Diego",
        "phone": "(619)562-0888",
        "email": "store4287@theupsstore.com",
        "longitude": -116.987622,
        "latitude": 32.837353,
        "googlePlaceId": None,
        "referenceId": "TUPSS4287",
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-03-13T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-13T19:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-03-13T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-13T19:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-03-13T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-13T19:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-03-13T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-13T19:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-03-13T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-13T19:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-03-13T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-13T14:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "fd51f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "The UPS Store 0007",
        "displayName": "PrintScan | UPS Store 0007 - SAN DIEGO, CA",
        "description": None,
        "metaDescription": "Explore PrintScan in San Diego, California for comprehensive Live Scan and Fingerprinting services. We provide swift, accurate, and professional solutions to meet your identification needs.",
        "notes": "Explore PrintScan in San Diego, California for comprehensive Live Scan and Fingerprinting services. We provide swift, accurate, and professional solutions to meet your identification needs.",
        "address1": "302 WASHINGTON ST",
        "address2": "",
        "stateCountry": "CA",
        "city": "SAN DIEGO",
        "postalCode": "92103",
        "county": "San Diego",
        "phone": "(619)291-5678",
        "email": "store0007@theupsstore.com",
        "longitude": -117.162641,
        "latitude": 32.750303,
        "googlePlaceId": None,
        "referenceId": "TUPSS0007",
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2024-01-23T14:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T19:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2024-01-23T14:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T19:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2024-01-23T14:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T19:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2024-01-23T14:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T19:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2024-01-23T14:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T19:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2024-01-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "0052f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "The UPS Store 0090",
        "displayName": "PrintScan | UPS Store 0090 - SAN DIEGO, CA",
        "description": None,
        "metaDescription": "Explore PrintScan in San Diego, California for comprehensive Live Scan and Fingerprinting services. We provide swift, accurate, and professional solutions to meet your identification needs.",
        "notes": "Explore PrintScan in San Diego, California for comprehensive Live Scan and Fingerprinting services. We provide swift, accurate, and professional solutions to meet your identification needs.",
        "address1": "501 W BROADWAY",
        "address2": "STE A",
        "stateCountry": "CA",
        "city": "SAN DIEGO",
        "postalCode": "92101-3562",
        "county": "San Diego",
        "phone": "(619)232-0332",
        "email": "store0090@theupsstore.com",
        "longitude": -117.168050,
        "latitude": 32.715501,
        "googlePlaceId": None,
        "referenceId": "TUPSS0090",
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2024-01-23T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T18:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2024-01-23T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T18:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2024-01-23T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T18:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2024-01-23T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T18:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2024-01-23T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T18:30:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2024-01-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "0d52f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "The UPS Store 0402",
        "displayName": "PrintScan | UPS Store 0402 - SEATTLE, WA",
        "description": None,
        "metaDescription": "Explore PrintScan in Seattle, Washington, the leading provider of Live Scan and Fingerprinting services. Offering efficient, accurate, and secure identification solutions to cater to your specific requirements.",
        "notes": "Explore PrintScan in Seattle, Washington, the leading provider of Live Scan and Fingerprinting services. Offering efficient, accurate, and secure identification solutions to cater to your specific requirements.",
        "address1": "800 FIFTH AVE",
        "address2": "STE 101",
        "stateCountry": "WA",
        "city": "SEATTLE",
        "postalCode": "98104-3102",
        "county": "King",
        "phone": "(206)382-9177",
        "email": "store0402@theupsstore.com",
        "longitude": -122.330291,
        "latitude": 47.605839,
        "googlePlaceId": None,
        "referenceId": "TUPSS0402",
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2022-04-22T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-04-22T18:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2022-04-22T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-04-22T18:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2022-04-22T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-04-22T18:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2022-04-22T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-04-22T18:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2022-04-22T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-04-22T18:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "1652f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "The UPS Store 2206",
        "displayName": "PrintScan | UPS Store 2206 - EAGLE RIVER, AK",
        "description": None,
        "metaDescription": "Choose PrintScan in Eagle River, Alaska, for high-quality Live Scan and Fingerprinting services. We provide fast, reliable, and secure identity verification solutions, tailored to meet your unique needs.",
        "notes": "Choose PrintScan in Eagle River, Alaska, for high-quality Live Scan and Fingerprinting services. We provide fast, reliable, and secure identity verification solutions, tailored to meet your unique needs.",
        "address1": "12110 BUSINESS BLVD",
        "address2": "STE A06",
        "stateCountry": "AK",
        "city": "EAGLE RIVER",
        "postalCode": "99577",
        "county": "Anchorage",
        "phone": "(907)694-7447",
        "email": "store2206@theupsstore.com",
        "longitude": -149.569851,
        "latitude": 61.330285,
        "googlePlaceId": None,
        "referenceId": "TUPSS2206",
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2024-01-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T19:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2024-01-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T19:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2024-01-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T19:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2024-01-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T19:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2024-01-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T19:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2024-01-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "2352f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "The UPS Store 3604",
        "displayName": "PrintScan | UPS Store 3604 - PORTLAND, OR",
        "description": None,
        "metaDescription": "Visit PrintScan in Portland, Oregon, your trusted destination for Live Scan and Fingerprinting services. Experience our efficient, precise, and secure identity confirmation solutions, tailored to meet your unique requirements.",
        "notes": "Visit PrintScan in Portland, Oregon, your trusted destination for Live Scan and Fingerprinting services. Experience our efficient, precise, and secure identity confirmation solutions, tailored to meet your unique requirements.",
        "address1": "818 SW 3RD AVE",
        "address2": "",
        "stateCountry": "OR",
        "city": "PORTLAND",
        "postalCode": "97204-2405",
        "county": "Multnomah",
        "phone": "(503)222-4888",
        "email": "store3604@theupsstore.com",
        "longitude": -122.675717,
        "latitude": 45.517246,
        "googlePlaceId": None,
        "referenceId": "TUPSS3604",
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 0,
                "timeOpen": "2024-01-23T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T15:00:00+00:00"
            },
            {
                "dayOfWeek": 1,
                "timeOpen": "2024-01-23T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T19:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2024-01-23T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T19:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2024-01-23T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T19:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2024-01-23T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T19:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2024-01-23T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T19:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2024-01-23T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "3f52f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "The UPS Store 4223",
        "displayName": "PrintScan | UPS Store 4223 - ATLANTA, GA",
        "description": None,
        "metaDescription": "Explore PrintScan in Atlanta, Georgia, the premier destination for advanced Live Scan and Fingerprinting services. We provide secure, swift, and dependable solutions, making us your go-to choice for all identification needs.",
        "notes": "Explore PrintScan in Atlanta, Georgia, the premier destination for advanced Live Scan and Fingerprinting services. We provide secure, swift, and dependable solutions, making us your go-to choice for all identification needs.",
        "address1": "3577-A CHAMBLEE TUCKER RD",
        "address2": "",
        "stateCountry": "GA",
        "city": "ATLANTA",
        "postalCode": "30341",
        "county": "Dekalb",
        "phone": "(678)209-1203",
        "email": "store4223@theupsstore.com",
        "longitude": -84.247765,
        "latitude": 33.883304,
        "googlePlaceId": None,
        "referenceId": "TUPSS4223",
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2024-01-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T19:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2024-01-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T19:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2024-01-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T19:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2024-01-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T19:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2024-01-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T19:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2024-01-23T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T18:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "1c53f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "The UPS Store 3687",
        "displayName": "PrintScan | UPS Store 3687 - LATHAM, NY",
        "description": None,
        "metaDescription": "Visit PrintScan in Latham, New York for exceptional Live Scan and Fingerprinting services. We prioritize your security with our accurate, fast, and reliable identity verification solutions.",
        "notes": "Visit PrintScan in Latham, New York for exceptional Live Scan and Fingerprinting services. We prioritize your security with our accurate, fast, and reliable identity verification solutions.",
        "address1": "595 NEW LOUDON RD",
        "address2": "",
        "stateCountry": "NY",
        "city": "LATHAM",
        "postalCode": "12110-4026",
        "county": "Albany",
        "phone": "(518)786-1925",
        "email": "store3687@theupsstore.com",
        "longitude": -73.759824,
        "latitude": 42.727582,
        "googlePlaceId": None,
        "referenceId": "TUPSS3687",
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2024-01-23T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T18:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2024-01-23T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T18:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2024-01-23T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T18:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2024-01-23T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T18:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2024-01-23T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T18:30:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2024-01-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-01-23T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "0454f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "Printscan - Hicksville Service Stations",
        "displayName": "Printscan - Hicksville",
        "description": "Located inside of the Quality Plaza Shopping Center",
        "metaDescription": "Rely on PrintScan in Hicksville, New York for exceptional Live Scan and Fingerprinting services. Our advanced technology ensures accurate and secure identity verification for your peace of mind.",
        "notes": "Rely on PrintScan in Hicksville, New York for exceptional Live Scan and Fingerprinting services. Our advanced technology ensures accurate and secure identity verification for your peace of mind.",
        "address1": "958 S Broadway",
        "address2": None,
        "stateCountry": "NY",
        "city": "Hicksville",
        "postalCode": "11801",
        "county": "Nassau",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -73.500150,
        "latitude": 40.744965,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:15:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:15:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:15:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:15:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:15:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "0554f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "Kings Park Shipping Center",
        "displayName": "Kings Park Shipping/Fingerprinting",
        "description": None,
        "metaDescription": "Get unparalleled Live Scan and Fingerprinting services at PrintScan in Kings Park, New York. We prioritize your security with our precise and trustworthy identity verification solutions.",
        "notes": "Get unparalleled Live Scan and Fingerprinting services at PrintScan in Kings Park, New York. We prioritize your security with our precise and trustworthy identity verification solutions.",
        "address1": "21 Pulaski Road",
        "address2": None,
        "stateCountry": "NY",
        "city": "Kings Park",
        "postalCode": "11754",
        "county": "Suffolk",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -73.258360,
        "latitude": 40.886100,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-06-20T10:00:00+00:00",
                "timeLunch": "2023-06-20T13:00:00+00:00",
                "timeResume": "2023-06-20T14:00:00+00:00",
                "timeClose": "2023-06-20T15:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-06-16T10:00:00+00:00",
                "timeLunch": "2023-06-16T13:00:00+00:00",
                "timeResume": "2023-06-16T14:00:00+00:00",
                "timeClose": "2023-06-16T15:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-06-16T10:00:00+00:00",
                "timeLunch": "2023-06-16T13:00:00+00:00",
                "timeResume": "2023-06-16T14:00:00+00:00",
                "timeClose": "2023-06-16T15:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-06-16T10:00:00+00:00",
                "timeLunch": "2023-06-16T13:00:00+00:00",
                "timeResume": "2023-06-16T14:00:00+00:00",
                "timeClose": "2023-06-16T15:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-06-16T10:00:00+00:00",
                "timeLunch": "2023-06-16T13:00:00+00:00",
                "timeResume": "2023-06-16T14:00:00+00:00",
                "timeClose": "2023-06-16T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "0654f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "Westchester Business Center",
        "displayName": "Printscan Authorized Fingerprint Service Center - White Plains, NY",
        "description": None,
        "metaDescription": "Visit PrintScan in White Plains, New York for superior Live Scan and Fingerprinting services. We are dedicated to providing secure and accurate identity verification for your utmost convenience.",
        "notes": "Visit PrintScan in White Plains, New York for superior Live Scan and Fingerprinting services. We are dedicated to providing secure and accurate identity verification for your utmost convenience.",
        "address1": "75 S Broadway",
        "address2": "4th Floor",
        "stateCountry": "NY",
        "city": "White Plains",
        "postalCode": "10601",
        "county": "Westchester",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -73.762771,
        "latitude": 41.029720,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-06-23T09:45:00+00:00",
                "timeLunch": "2023-06-23T12:30:00+00:00",
                "timeResume": "2023-06-23T14:00:00+00:00",
                "timeClose": "2023-06-23T15:45:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-06-23T09:45:00+00:00",
                "timeLunch": "2023-06-23T12:30:00+00:00",
                "timeResume": "2023-06-23T14:00:00+00:00",
                "timeClose": "2023-06-23T15:45:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-06-23T09:45:00+00:00",
                "timeLunch": "2023-06-23T12:30:00+00:00",
                "timeResume": "2023-06-23T14:00:00+00:00",
                "timeClose": "2023-06-23T15:45:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-06-23T09:45:00+00:00",
                "timeLunch": "2023-06-23T12:30:00+00:00",
                "timeResume": "2023-06-23T14:00:00+00:00",
                "timeClose": "2023-06-23T15:45:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-07-07T09:45:00+00:00",
                "timeLunch": "2023-07-07T12:30:00+00:00",
                "timeResume": "2023-07-07T14:00:00+00:00",
                "timeClose": "2023-07-07T14:45:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "3e54f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "Louisiana Firearms",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Baton Rouge, LA",
        "description": "Located inside Louisiana Firearms",
        "metaDescription": "Visit PrintScan in Baton Rouge, Louisiana, for superior Live Scan and Fingerprinting services. We provide fast, secure, and personalized identification solutions to meet your unique requirements.",
        "notes": "Visit PrintScan in Baton Rouge, Louisiana, for superior Live Scan and Fingerprinting services. We provide fast, secure, and personalized identification solutions to meet your unique requirements.",
        "address1": "9634 Airline Highway",
        "address2": "Suite F3",
        "stateCountry": "LA",
        "city": "Baton Rouge",
        "postalCode": "70815",
        "county": "East Baton Rouge",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -91.083799,
        "latitude": 30.431781,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "7654f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "Axel Protection Services Inc.",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Jamaica, NY",
        "description": None,
        "metaDescription": "Turn to PrintScan in Jamaica, New York for exceptional Live Scan and Fingerprinting services. We are dedicated to providing secure and accurate identification solutions tailored to your needs.",
        "notes": "Turn to PrintScan in Jamaica, New York for exceptional Live Scan and Fingerprinting services. We are dedicated to providing secure and accurate identification solutions tailored to your needs.",
        "address1": "90-24 161st Street",
        "address2": None,
        "stateCountry": "NY",
        "city": "Jamaica",
        "postalCode": "11432",
        "county": "Queens",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -73.799216,
        "latitude": 40.704729,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-06-29T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-29T18:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-06-29T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-29T18:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-06-29T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-29T18:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-06-29T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-29T18:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-06-29T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-29T18:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-06-29T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-29T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "7754f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "Metropolitan Special Services",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Flatbush Kiosk Location",
        "description": None,
        "metaDescription": "Welcome to PrintScan in Brooklyn, New York, your reliable provider for top-notch Live Scan and Fingerprinting services. Enjoy our speedy, secure, and trusted fingerprinting offerings at PrintScan Brooklyn today.",
        "notes": "Welcome to PrintScan in Brooklyn, New York, your reliable provider for top-notch Live Scan and Fingerprinting services. Enjoy our speedy, secure, and trusted fingerprinting offerings at PrintScan Brooklyn today.",
        "address1": "1772 Flatbush Ave",
        "address2": None,
        "stateCountry": "NY",
        "city": "Brooklyn",
        "postalCode": "11210",
        "county": "Kings",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -73.941633,
        "latitude": 40.626684,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-07-31T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-31T16:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-07-31T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-31T16:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-07-31T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-31T16:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-07-31T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-31T16:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-07-31T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-31T16:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "7954f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "SCI Security Training",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Woodside Kiosk",
        "description": None,
        "metaDescription": "Rely on PrintScan in Woodside, New York for high-quality Live Scan and Fingerprinting services. Our commitment to accuracy and security makes us a trusted choice for all your identification needs.",
        "notes": "Rely on PrintScan in Woodside, New York for high-quality Live Scan and Fingerprinting services. Our commitment to accuracy and security makes us a trusted choice for all your identification needs.",
        "address1": "3119 56th Street, suite C8",
        "address2": None,
        "stateCountry": "NY",
        "city": "Woodside",
        "postalCode": "11377",
        "county": "Queens",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -73.905377,
        "latitude": 40.756729,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "7a54f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "Nightlife Security",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Bronx, NY",
        "description": None,
        "metaDescription": "Visit PrintScan in Bronx, New York for premium Live Scan and Fingerprinting services. Our team is dedicated to providing secure, efficient, and accurate identification solutions to meet your specific needs.",
        "notes": "Visit PrintScan in Bronx, New York for premium Live Scan and Fingerprinting services. Our team is dedicated to providing secure, efficient, and accurate identification solutions to meet your specific needs.",
        "address1": "2114  Williamsbridge Road, Suite 114",
        "address2": "Lower Level",
        "stateCountry": "NY",
        "city": "Bronx",
        "postalCode": "10461",
        "county": "Bronx",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -73.855315,
        "latitude": 40.855961,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T12:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T12:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T12:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T12:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T12:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "7f54f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "E Identity Services",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Saint Peters, MO",
        "description": "Between McClay Rd & Queensbrooke Blvd, in Ashleigh Place",
        "metaDescription": "Choose PrintScan in Saint Peters, Missouri for superior Live Scan and Fingerprinting services. Our dedicated team ensures precise, secure, and efficient services to meet all your identification needs.",
        "notes": "Choose PrintScan in Saint Peters, Missouri for superior Live Scan and Fingerprinting services. Our dedicated team ensures precise, secure, and efficient services to meet all your identification needs.",
        "address1": "1405 Jungermann Rd",
        "address2": "Suite B",
        "stateCountry": "MO",
        "city": "Saint Peters",
        "postalCode": "63376",
        "county": "Saint Charles",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -90.586840,
        "latitude": 38.753263,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": "2000-01-01T13:00:00+00:00",
                "timeResume": "2000-01-01T14:00:00+00:00",
                "timeClose": "2000-01-01T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": "2000-01-01T13:00:00+00:00",
                "timeResume": "2000-01-01T14:00:00+00:00",
                "timeClose": "2000-01-01T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": "2000-01-01T13:00:00+00:00",
                "timeResume": "2000-01-01T14:00:00+00:00",
                "timeClose": "2000-01-01T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "8054f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "INDIAN VISA CENTERS",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Floral Park, Queens",
        "description": None,
        "metaDescription": "Visit PrintScan in Floral Park, New York for premium Live Scan and Fingerprinting services. We are committed to providing secure, accurate, and efficient identification solutions tailored to your specific needs.",
        "notes": "Visit PrintScan in Floral Park, New York for premium Live Scan and Fingerprinting services. We are committed to providing secure, accurate, and efficient identification solutions tailored to your specific needs.",
        "address1": "261-03 Hillside Ave",
        "address2": None,
        "stateCountry": "NY",
        "city": "Floral Park",
        "postalCode": "11004",
        "county": "Queens",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -73.707294,
        "latitude": 40.737794,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-29T12:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T18:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-29T12:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T18:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-29T12:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T18:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-29T12:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T18:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-29T12:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T18:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "8154f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "Paralegals FTC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Union City Kiosk Location",
        "description": None,
        "metaDescription": "Trust PrintScan in Union City, New Jersey for your Live Scan and Fingerprinting needs. We offer secure, precise, and efficient identification services to ensure your peace of mind.",
        "notes": "Trust PrintScan in Union City, New Jersey for your Live Scan and Fingerprinting needs. We offer secure, precise, and efficient identification services to ensure your peace of mind.",
        "address1": "1912 Bergenline Ave",
        "address2": None,
        "stateCountry": "NJ",
        "city": "Union City",
        "postalCode": "07087",
        "county": "Hudson",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -74.034223,
        "latitude": 40.764615,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T11:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:45:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T11:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:45:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T12:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T12:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "8654f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "Mail Center Etc.",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Atlanta Kiosk Location",
        "description": "DUNWOODY LOCATION",
        "metaDescription": "Choose PrintScan in Dunwoody, Georgia for superior Live Scan and Fingerprinting services. We offer secure, efficient, and accurate identification solutions to meet your unique needs.",
        "notes": "Choose PrintScan in Dunwoody, Georgia for superior Live Scan and Fingerprinting services. We offer secure, efficient, and accurate identification solutions to meet your unique needs.",
        "address1": "5579 Chamblee Dunwoody Road",
        "address2": "B",
        "stateCountry": "GA",
        "city": "Dunwoody",
        "postalCode": "30338",
        "county": "Dekalb",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -84.336028,
        "latitude": 33.950732,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-05-08T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-08T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-05-08T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-08T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-05-08T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-08T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-05-08T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-08T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-09-07T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-07T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "8854f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "33-Leah's Postal Services, Inc DBA: LA Postal Cent",
        "displayName": "PrintScan - Authorized Fingerprint Service Center -Los Angeles, CA",
        "description": None,
        "metaDescription": "Turn to PrintScan in Sherman Oaks, California for high-quality Live Scan and Fingerprinting services. We are dedicated to providing secure, efficient, and precise identification solutions for all our clients.",
        "notes": "Turn to PrintScan in Sherman Oaks, California for high-quality Live Scan and Fingerprinting services. We are dedicated to providing secure, efficient, and precise identification solutions for all our clients.",
        "address1": "15021 Ventura Blvd",
        "address2": None,
        "stateCountry": "CA",
        "city": "Sherman Oaks",
        "postalCode": "91403",
        "county": "Los Angeles",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -118.460343,
        "latitude": 34.152993,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-06-14T09:30:00+00:00",
                "timeLunch": "2023-06-14T13:00:00+00:00",
                "timeResume": "2023-06-14T14:00:00+00:00",
                "timeClose": "2023-06-14T17:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-06-14T09:30:00+00:00",
                "timeLunch": "2023-06-14T13:00:00+00:00",
                "timeResume": "2023-06-14T14:00:00+00:00",
                "timeClose": "2023-06-14T17:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-06-14T09:30:00+00:00",
                "timeLunch": "2023-06-14T13:00:00+00:00",
                "timeResume": "2023-06-14T14:00:00+00:00",
                "timeClose": "2023-06-14T17:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-06-14T09:30:00+00:00",
                "timeLunch": "2023-06-14T13:00:00+00:00",
                "timeResume": "2023-06-14T14:00:00+00:00",
                "timeClose": "2023-06-14T17:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-06-14T09:30:00+00:00",
                "timeLunch": "2023-06-14T13:00:00+00:00",
                "timeResume": "2023-06-14T14:00:00+00:00",
                "timeClose": "2023-06-14T17:30:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "8b54f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "NE Test Centers - Rockland, MA",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Rockland, MA",
        "description": None,
        "metaDescription": "Trust PrintScan in Rockland, Massachusetts for all your Live Scan and Fingerprinting requirements. We deliver secure, swift, and accurate identification services, tailored to meet your specific needs.",
        "notes": "Trust PrintScan in Rockland, Massachusetts for all your Live Scan and Fingerprinting requirements. We deliver secure, swift, and accurate identification services, tailored to meet your specific needs.",
        "address1": "100 Ledgewood place",
        "address2": "204A",
        "stateCountry": "MA",
        "city": "Rockland",
        "postalCode": "02370",
        "county": "Plymouth",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -70.908099,
        "latitude": 42.161914,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 2,
                "timeOpen": "2022-07-28T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-07-28T14:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2022-07-28T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-07-28T14:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "9354f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "River Region Training and Development Center",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Laplace, LA",
        "description": None,
        "metaDescription": "Choose PrintScan in Laplace, Louisiana for your Live Scan and Fingerprinting needs. We are committed to providing secure, efficient, and accurate identification services, tailored to your unique requirements.",
        "notes": "Choose PrintScan in Laplace, Louisiana for your Live Scan and Fingerprinting needs. We are committed to providing secure, efficient, and accurate identification services, tailored to your unique requirements.",
        "address1": "2925 US Hwy 51",
        "address2": "Suite D",
        "stateCountry": "LA",
        "city": "Laplace",
        "postalCode": "70068",
        "county": "St John The Baptist",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -90.447049,
        "latitude": 30.087919,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:30:00+00:00",
                "timeLunch": "2000-01-01T12:00:00+00:00",
                "timeResume": "2000-01-01T12:30:00+00:00",
                "timeClose": "2000-01-01T15:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:30:00+00:00",
                "timeLunch": "2000-01-01T12:00:00+00:00",
                "timeResume": "2000-01-01T12:30:00+00:00",
                "timeClose": "2000-01-01T15:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:30:00+00:00",
                "timeLunch": "2000-01-01T12:00:00+00:00",
                "timeResume": "2000-01-01T12:30:00+00:00",
                "timeClose": "2000-01-01T15:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:30:00+00:00",
                "timeLunch": "2000-01-01T12:00:00+00:00",
                "timeResume": "2000-01-01T12:30:00+00:00",
                "timeClose": "2000-01-01T15:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:30:00+00:00",
                "timeLunch": "2000-01-01T12:00:00+00:00",
                "timeResume": "2000-01-01T12:30:00+00:00",
                "timeClose": "2000-01-01T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "9454f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "Postal Annex",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Miami Kiosk Location",
        "description": "Located in the Shops at Skylake",
        "metaDescription": "Discover PrintScan in North Miami Beach, Florida, your go-to place for exceptional Live Scan and Fingerprinting services. Benefit from our quick, secure, and tailored solutions designed to meet your individual requirements.",
        "notes": "Discover PrintScan in North Miami Beach, Florida, your go-to place for exceptional Live Scan and Fingerprinting services. Benefit from our quick, secure, and tailored solutions designed to meet your individual requirements.",
        "address1": "1728 NE Miami Gardens Dr.",
        "address2": None,
        "stateCountry": "FL",
        "city": "North Miami Beach",
        "postalCode": "33179",
        "county": "Miami-Dade",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.165251,
        "latitude": 25.944580,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 0,
                "timeOpen": "2022-06-06T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-06-06T13:30:00+00:00"
            },
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2022-04-20T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-04-20T18:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:30:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2022-06-06T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-06-06T15:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "9654f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "Besta Care",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Longwood, FL",
        "description": None,
        "metaDescription": "Turn to PrintScan in Longwood, Florida for high-quality Live Scan and Fingerprinting services. Our dedicated team ensures secure, swift, and precise identification solutions for all your needs.",
        "notes": "Turn to PrintScan in Longwood, Florida for high-quality Live Scan and Fingerprinting services. Our dedicated team ensures secure, swift, and precise identification solutions for all your needs.",
        "address1": "1200 West State Road 434",
        "address2": "Suite 221",
        "stateCountry": "FL",
        "city": "Longwood",
        "postalCode": "32750",
        "county": "Seminole",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.368723,
        "latitude": 28.697478,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "9a54f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "Gina S Duncan Insurance Agency, LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Upper Marlboro, MD",
        "description": None,
        "metaDescription": "Visit PrintScan in Upper Marlboro, Maryland, your premier destination for superior Live Scan and Fingerprinting services. Experience our speedy, precise, and trustworthy solutions now!",
        "notes": "Visit PrintScan in Upper Marlboro, Maryland, your premier destination for superior Live Scan and Fingerprinting services. Experience our speedy, precise, and trustworthy solutions now!",
        "address1": "1401 Mercantile Lane",
        "address2": "Ste 251",
        "stateCountry": "MD",
        "city": "Upper Marlboro",
        "postalCode": "20774",
        "county": "Prince Georges",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -76.836744,
        "latitude": 38.909325,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "a654f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "Genesis Finger Prints",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Clovis, NM",
        "description": None,
        "metaDescription": "Get efficient and precise Live Scan and Fingerprinting services at PrintScan in Clovis, New Mexico. Our dedicated team is committed to providing fast and accurate identification solutions. Rely on PrintScan Clovis, NM for all your fingerprinting needs.",
        "notes": "Get efficient and precise Live Scan and Fingerprinting services at PrintScan in Clovis, New Mexico. Our dedicated team is committed to providing fast and accurate identification solutions. Rely on PrintScan Clovis, NM for all your fingerprinting needs.",
        "address1": "716 Mitchell St",
        "address2": None,
        "stateCountry": "NM",
        "city": "Clovis",
        "postalCode": "88101",
        "county": "Curry",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -103.206865,
        "latitude": 34.405446,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00+00:00",
                "timeResume": "2000-01-01T13:00:00+00:00",
                "timeClose": "2000-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00+00:00",
                "timeResume": "2000-01-01T13:00:00+00:00",
                "timeClose": "2000-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00+00:00",
                "timeResume": "2000-01-01T13:00:00+00:00",
                "timeClose": "2000-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T08:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00+00:00",
                "timeResume": "2000-01-01T13:00:00+00:00",
                "timeClose": "2000-01-01T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b054f51c-fed8-eb11-a7ad-000d3a12961f",
        "name": "Comforting, Loving & Helping Hands Home Care",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Longwood, FL",
        "description": None,
        "metaDescription": "Turn to PrintScan in Longwood, Florida for high-quality Live Scan and Fingerprinting services. Our dedicated team ensures secure, swift, and precise identification solutions for all your needs.",
        "notes": "Turn to PrintScan in Longwood, Florida for high-quality Live Scan and Fingerprinting services. Our dedicated team ensures secure, swift, and precise identification solutions for all your needs.",
        "address1": "1414 N Ronald Reagan Blvd",
        "address2": "Suite 1220",
        "stateCountry": "FL",
        "city": "Longwood",
        "postalCode": "32750",
        "county": "Seminole",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.342896,
        "latitude": 28.714357,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T10:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T13:30:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-07-10T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-10T15:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:30:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:30:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T13:30:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "d7fd7f21-90e5-eb11-a7ad-000d3a12961f",
        "name": "Piece of Mind Firearms",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Triadelphia, WV",
        "description": None,
        "metaDescription": "Discover top-notch Live Scan and Fingerprinting services at PrintScan in Triadelphia, West Virginia. Our dedicated team delivers precise and quick results, making us your go-to destination for all identification requirements. Choose PrintScan Triadelphia for dependable fingerprinting solutions.",
        "notes": "Discover top-notch Live Scan and Fingerprinting services at PrintScan in Triadelphia, West Virginia. Our dedicated team delivers precise and quick results, making us your go-to destination for all identification requirements. Choose PrintScan Triadelphia for dependable fingerprinting solutions.",
        "address1": "241 Gashell Run Road",
        "address2": None,
        "stateCountry": "WV",
        "city": "Triadelphia",
        "postalCode": "26059",
        "county": "Ohio",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.608624,
        "latitude": 40.070222,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T12:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "99b80917-7f11-ec11-981f-000d3a1330e1",
        "name": "PRIVATE EVENT - Mobile Pre-Enroll",
        "displayName": "PRIVATE EVENT - Mobile Pre-Enroll",
        "description": "DO NOT SELECT UNLESS YOU WERE ADVISED TO DO SO!",
        "metaDescription": "Join us at our PrintScan Event in New York for premier Live Scan and Fingerprinting services. Our expert team delivers fast and accurate results for all your identification needs. Choose PrintScan New York for reliable, efficient, and professional fingerprinting solutions at our special event.",
        "notes": "Join us at our PrintScan Event in New York for premier Live Scan and Fingerprinting services. Our expert team delivers fast and accurate results for all your identification needs. Choose PrintScan New York for reliable, efficient, and professional fingerprinting solutions at our special event.",
        "address1": "Mobile",
        "address2": None,
        "stateCountry": "NY",
        "city": "Event",
        "postalCode": "11801",
        "county": "NY",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -73.528813,
        "latitude": 40.766203,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2022-08-01T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-08-01T20:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2022-08-01T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-08-01T20:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2022-08-01T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-08-01T20:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2022-08-01T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-08-01T20:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2022-08-01T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-08-01T20:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "ca1ccb87-4b35-ee11-a3ef-000d3a4d54f8",
        "name": "Qwikpack LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Bridgeport, CT",
        "description": None,
        "metaDescription": "Choose PrintScan in Bridgeport, Connecticut for your Live Scan and Fingerprinting needs. Our professional team delivers swift and precise services for all your identification requirements. Stop by our location today!",
        "notes": "Choose PrintScan in Bridgeport, Connecticut for your Live Scan and Fingerprinting needs. Our professional team delivers swift and precise services for all your identification requirements. Stop by our location today!",
        "address1": "1019 Main St.",
        "address2": None,
        "stateCountry": "CT",
        "city": "Bridgeport",
        "postalCode": "06604",
        "county": "Fairfield",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -73.189325,
        "latitude": 41.178386,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-29T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T16:45:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-29T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T16:45:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-29T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T16:45:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-29T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T16:45:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-29T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T16:45:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "0dbf896f-773c-ee11-a3ef-000d3a4d54f8",
        "name": "ARCPoint Labs of Martinez",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Martinez, CA",
        "description": None,
        "metaDescription": "Experience the best in Live Scan and Fingerprinting services at PrintScan in Martinez, California. We offer secure, high-quality identification solutions, ensuring your needs are met with precision and efficiency.",
        "notes": "Experience the best in Live Scan and Fingerprinting services at PrintScan in Martinez, California. We offer secure, high-quality identification solutions, ensuring your needs are met with precision and efficiency.",
        "address1": "3237 Alhambra Avenue",
        "address2": "#2",
        "stateCountry": "CA",
        "city": "Martinez",
        "postalCode": "94553",
        "county": "Contra Costa",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -122.131270,
        "latitude": 38.001269,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-09-15T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-15T15:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-09-15T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-15T15:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-09-15T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-15T15:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-09-15T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-15T15:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-09-15T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-15T15:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "c7407114-793c-ee11-a3ef-000d3a4d54f8",
        "name": "ARCPoint Labs of San Rafael",
        "displayName": "PrintScan Authorized Fingerprint Service Center - San Rafael, CA",
        "description": None,
        "metaDescription": "Experience high-quality Live Scan and Fingerprinting services at PrintScan in San Rafael, California. Our dedicated team ensures accurate and quick results for all your identification needs. Visit us today!",
        "notes": "Experience high-quality Live Scan and Fingerprinting services at PrintScan in San Rafael, California. Our dedicated team ensures accurate and quick results for all your identification needs. Visit us today!",
        "address1": "4340 Redwood Highway",
        "address2": "STE A33",
        "stateCountry": "CA",
        "city": "San Rafael",
        "postalCode": "94903",
        "county": "Marin",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -122.540034,
        "latitude": 38.016261,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-09-11T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-11T14:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-09-11T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-11T14:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-09-11T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-11T14:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-09-11T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-11T14:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-09-11T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-11T14:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "7519f0be-2241-ee11-a3ef-000d3a4d54f8",
        "name": "Speedy Post LLC DBA Qwik Pack & Ship",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Fort Walton Beach, FL",
        "description": None,
        "metaDescription": "Experience PrintScan in Fort Walton Beach, Florida, your reliable choice for exceptional Live Scan and Fingerprinting services. Take advantage of our precise, speedy, and trustworthy solutions for all your identification necessities.",
        "notes": "Experience PrintScan in Fort Walton Beach, Florida, your reliable choice for exceptional Live Scan and Fingerprinting services. Take advantage of our precise, speedy, and trustworthy solutions for all your identification necessities.",
        "address1": "913 Beal Parkway NW",
        "address2": "Suite A",
        "stateCountry": "FL",
        "city": "Fort Walton Beach",
        "postalCode": "32547",
        "county": "Okaloosa",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -86.637570,
        "latitude": 30.450844,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "298fc8fa-9142-ee11-a3ef-000d3a4d54f8",
        "name": "Total Protection Solution LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - West Palm Beach, FL",
        "description": None,
        "metaDescription": "Choose PrintScan in West Palm Beach, Florida for top-quality Live Scan and Fingerprinting services. Our commitment to accuracy and security makes us your trusted partner for all identity verification needs.",
        "notes": "Choose PrintScan in West Palm Beach, Florida for top-quality Live Scan and Fingerprinting services. Our commitment to accuracy and security makes us your trusted partner for all identity verification needs.",
        "address1": "2695 North Military Trail",
        "address2": "Suite #5",
        "stateCountry": "FL",
        "city": "West Palm Beach",
        "postalCode": "33409",
        "county": "Palm Beach",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.111233,
        "latitude": 26.716962,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:30:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:30:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:30:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:30:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:30:00-04:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-09-15T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:30:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "2ca151af-5d43-ee11-a3ef-000d3a4d54f8",
        "name": "ARCPoint Labs of Santa Ana",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Santa Ana, CA",
        "description": None,
        "metaDescription": "Explore premier Live Scan and Fingerprinting solutions at PrintScan in Santa Ana, California. Benefit from our swift, dependable, and expert services designed to cater to your specific requirements. Rely on PrintScan Santa Ana, CA for all your identification needs.",
        "notes": "Explore premier Live Scan and Fingerprinting solutions at PrintScan in Santa Ana, California. Benefit from our swift, dependable, and expert services designed to cater to your specific requirements. Rely on PrintScan Santa Ana, CA for all your identification needs.",
        "address1": "3500 South Bristol St",
        "address2": "STE 205",
        "stateCountry": "CA",
        "city": "Santa Ana",
        "postalCode": "92704",
        "county": "Orange",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -117.886146,
        "latitude": 33.700410,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:30:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-07:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:30:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-07:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:30:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-07:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:30:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-07:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:30:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-07:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "4740ea6a-7447-ee11-a3ef-000d3a4d54f8",
        "name": "Package Central",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Sandusky, OH",
        "description": None,
        "metaDescription": "Experience top-notch Live Scan and Fingerprinting services at PrintScan in Sandusky, Ohio. Utilize our fast, reliable, and expert services, customized to suit your specific needs. Choose PrintScan Sandusky, OH for all your advanced identification requirements.",
        "notes": "Experience top-notch Live Scan and Fingerprinting services at PrintScan in Sandusky, Ohio. Utilize our fast, reliable, and expert services, customized to suit your specific needs. Choose PrintScan Sandusky, OH for all your advanced identification requirements.",
        "address1": "2012 East Perkins Avenue",
        "address2": None,
        "stateCountry": "OH",
        "city": "Sandusky",
        "postalCode": "44870",
        "county": "Erie",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -82.668471,
        "latitude": 41.428463,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-30T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-30T16:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-30T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-30T16:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-30T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-30T16:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-30T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-30T16:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-30T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-30T16:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "5f52e9f2-da5b-ee11-9935-000d3a4fda52",
        "name": "Black Hat Enterprises, Inc. dba Mailboxes & Beyond",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Blytheville, AR",
        "description": None,
        "metaDescription": "Explore PrintScan in Blytheville, Arkansas, your trusted provider for premium Live Scan and Fingerprinting services. Choose PrintScan for fast, accurate, and secure identification solutions. Explore PrintScan in Blytheville, Arkansas, your trusted provider for premium Live Scan and Fingerprinting services. Choose PrintScan for fast, accurate, and secure identification solutions.",
        "notes": "Explore PrintScan in Blytheville, Arkansas, your trusted provider for premium Live Scan and Fingerprinting services. Choose PrintScan for fast, accurate, and secure identification solutions. Explore PrintScan in Blytheville, Arkansas, your trusted provider for premium Live Scan and Fingerprinting services. Choose PrintScan for fast, accurate, and secure identification solutions.",
        "address1": "103 W Main Street",
        "address2": None,
        "stateCountry": "AR",
        "city": "Blytheville",
        "postalCode": "72315",
        "county": "Mississippi",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -89.903000,
        "latitude": 35.927397,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:30:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "ca9188b2-db5b-ee11-9935-000d3a4fda52",
        "name": "Speedway Shipping Services, LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Port Orange, FL",
        "description": None,
        "metaDescription": "Find exceptional Live Scan and Fingerprinting services at PrintScan in Port Orange, Arizona. Take advantage of our speedy, trustworthy, and professional services, tailored to meet your unique needs. Depend on PrintScan Port Orange, AZ for all your comprehensive identification services.",
        "notes": "Find exceptional Live Scan and Fingerprinting services at PrintScan in Port Orange, Arizona. Take advantage of our speedy, trustworthy, and professional services, tailored to meet your unique needs. Depend on PrintScan Port Orange, AZ for all your comprehensive identification services.",
        "address1": "3761 S Nova Road",
        "address2": "Suite P",
        "stateCountry": "FL",
        "city": "Port Orange",
        "postalCode": "32129",
        "county": "Volusia",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.005581,
        "latitude": 29.130565,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-09-25T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-25T18:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-09-25T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-25T18:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-09-25T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-25T18:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-09-25T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-25T18:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-09-25T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-25T18:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-09-25T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-25T14:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "246f0656-dd5b-ee11-9935-000d3a4fda52",
        "name": "Edmond Parcels Plus",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Edmond, OK",
        "description": "Next door to Hobby Lobby",
        "metaDescription": "Visit PrintScan in Edmond, OK for exceptional Live Scan and Fingerprinting services. Benefit from our secure, swift, and customized solutions for all your identification requirements.",
        "notes": "Visit PrintScan in Edmond, OK for exceptional Live Scan and Fingerprinting services. Benefit from our secure, swift, and customized solutions for all your identification requirements.",
        "address1": "820 W Danforth Road.",
        "address2": None,
        "stateCountry": "OK",
        "city": "Edmond",
        "postalCode": "73003",
        "county": "Oklahoma County",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -97.494122,
        "latitude": 35.666422,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-09-25T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-25T18:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-09-25T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-25T18:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-09-25T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-25T18:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-09-25T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-25T18:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-09-25T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-25T18:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-09-25T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-25T14:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "736ef7b7-6e5c-ee11-9935-000d3a4fda52",
        "name": "Mail Mart USA",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Miami, FL",
        "description": None,
        "metaDescription": "Explore PrintScan in Miami, Florida, your premier choice for advanced Live Scan and Fingerprinting services. Benefit from our swift, secure, and dependable fingerprinting processes at PrintScan Miami today.",
        "notes": "Explore PrintScan in Miami, Florida, your premier choice for advanced Live Scan and Fingerprinting services. Benefit from our swift, secure, and dependable fingerprinting processes at PrintScan Miami today.",
        "address1": "13727 SW 152nd Street",
        "address2": None,
        "stateCountry": "FL",
        "city": "Miami",
        "postalCode": "33177",
        "county": "Miami-Dade",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.415322,
        "latitude": 25.627325,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-09-26T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-26T17:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-09-26T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-26T17:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-09-26T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-26T17:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-09-26T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-26T17:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-09-26T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-26T17:30:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-09-26T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-26T12:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "155b91e0-3156-ee11-9935-000d3a536176",
        "name": "Encore Healthcare Services LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Hannibal, MO",
        "description": None,
        "metaDescription": "Choose PrintScan in Hannibal, Missouri for exceptional Live Scan and Fingerprinting services. Our dedication to accuracy and speed in identification services sets us apart. Trust in PrintScan Hannibal for all your fingerprinting solutions.",
        "notes": "Choose PrintScan in Hannibal, Missouri for exceptional Live Scan and Fingerprinting services. Our dedication to accuracy and speed in identification services sets us apart. Trust in PrintScan Hannibal for all your fingerprinting solutions.",
        "address1": "2800 Saint Marys Ave",
        "address2": "Suite B",
        "stateCountry": "MO",
        "city": "Hannibal",
        "postalCode": "63401",
        "county": "Ralls",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -91.385912,
        "latitude": 39.705982,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "fd643d84-3256-ee11-9935-000d3a536176",
        "name": "YCP Shipping Solutions DBA Postal Connections 209",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - York, PA",
        "description": None,
        "metaDescription": "Explore top-tier Live Scan and Fingerprinting services at PrintScan in York, Pennsylvania. Our professional team delivers swift, accurate, and dependable results for all your identification requirements. Trust in PrintScan York for secure and streamlined services.",
        "notes": "Explore top-tier Live Scan and Fingerprinting services at PrintScan in York, Pennsylvania. Our professional team delivers swift, accurate, and dependable results for all your identification requirements. Trust in PrintScan York for secure and streamlined services.",
        "address1": "211 Pauline Drive",
        "address2": None,
        "stateCountry": "PA",
        "city": "York",
        "postalCode": "17402",
        "county": "York",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -76.682937,
        "latitude": 39.932634,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "c4432ca0-8a58-ee11-9935-000d3a536176",
        "name": "ARCpoint Labs of Oklahoma City",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Oklahoma City, OK",
        "description": "Next to Subway",
        "metaDescription": "Rely on PrintScan in Oklahoma City, OK for comprehensive Live Scan and Fingerprinting services. Experience our commitment to accuracy, efficiency, and excellent customer care.",
        "notes": "Rely on PrintScan in Oklahoma City, OK for comprehensive Live Scan and Fingerprinting services. Experience our commitment to accuracy, efficiency, and excellent customer care.",
        "address1": "2126 South Meridian Avenue",
        "address2": None,
        "stateCountry": "OK",
        "city": "Oklahoma City",
        "postalCode": "73108",
        "county": "Oklahoma",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -97.600608,
        "latitude": 35.443723,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-09-21T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-21T16:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-09-21T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-21T16:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-09-21T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-21T16:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-09-21T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-21T16:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-09-21T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-21T16:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "7bd0a9c6-e450-ee11-9935-000d3a55a2f5",
        "name": "B&B Evaluation Services",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Phoenix, AZ",
        "description": None,
        "metaDescription": "Visit PrintScan in Phoenix, Arizona, your premier source for professional Live Scan and Fingerprinting services. Benefit from our fast, secure, and dependable fingerprinting systems at PrintScan Phoenix today.",
        "notes": "Visit PrintScan in Phoenix, Arizona, your premier source for professional Live Scan and Fingerprinting services. Benefit from our fast, secure, and dependable fingerprinting systems at PrintScan Phoenix today.",
        "address1": "4022 E Broadway Rd",
        "address2": "Suite 118",
        "stateCountry": "AZ",
        "city": "Phoenix",
        "postalCode": "85040",
        "county": "Maricopa",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -111.993669,
        "latitude": 33.407846,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:45:00-07:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:45:00-07:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:45:00-07:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:45:00-07:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:45:00-07:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T09:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-07:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "f9a523b9-e850-ee11-9935-000d3a55a2f5",
        "name": "ER Services",
        "displayName": "PrintScan Authorized Fingerprint Service Center - East Wenatchee, WA",
        "description": "Next to Valley Mall Center",
        "metaDescription": "Visit PrintScan in East Wenatchee, Washington for premium Live Scan and Fingerprinting services. Our dedication to providing precise and swift identification services makes us a trusted choice. Rely on PrintScan East Wenatchee for all your fingerprinting needs.",
        "notes": "Visit PrintScan in East Wenatchee, Washington for premium Live Scan and Fingerprinting services. Our dedication to providing precise and swift identification services makes us a trusted choice. Rely on PrintScan East Wenatchee for all your fingerprinting needs.",
        "address1": "645 Valley Mall Parkway",
        "address2": "Suite #200",
        "stateCountry": "WA",
        "city": "East Wenatchee",
        "postalCode": "98802",
        "county": "Douglas",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -120.291719,
        "latitude": 47.413674,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T10:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-07:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-07:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-07:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-07:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-07:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "04527414-ea50-ee11-9935-000d3a55a2f5",
        "name": "LP Consultants",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Waltham, MA",
        "description": None,
        "metaDescription": "Experience top-tier Live Scan and Fingerprinting services at PrintScan in Waltham, Massachusetts. Our focus on accuracy and efficiency in identification services distinguishes us from the rest. Trust PrintScan Waltham for all your fingerprinting requirements.",
        "notes": "Experience top-tier Live Scan and Fingerprinting services at PrintScan in Waltham, Massachusetts. Our focus on accuracy and efficiency in identification services distinguishes us from the rest. Trust PrintScan Waltham for all your fingerprinting requirements.",
        "address1": "303 Wyman Street",
        "address2": "Suite 300",
        "stateCountry": "MA",
        "city": "Waltham",
        "postalCode": "02451",
        "county": "Middlesex",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -71.255403,
        "latitude": 42.406832,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "c9a05718-ec50-ee11-9935-000d3a55a2f5",
        "name": "Premiere Business Pursuits",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Columbia SC",
        "description": None,
        "metaDescription": "Choose PrintScan in Columbia, South Carolina for exceptional Live Scan and Fingerprinting services. Our professional team delivers accurate and fast identification solutions for all your needs.",
        "notes": "Choose PrintScan in Columbia, South Carolina for exceptional Live Scan and Fingerprinting services. Our professional team delivers accurate and fast identification solutions for all your needs.",
        "address1": "534 Saint Andrews Road",
        "address2": "Suite B",
        "stateCountry": "SC",
        "city": "Columbia",
        "postalCode": "29210",
        "county": "Richland",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.127593,
        "latitude": 34.044781,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T14:00:00-05:00",
                "timeClose": "2000-01-01T16:15:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T14:00:00-05:00",
                "timeClose": "2000-01-01T16:15:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T14:00:00-05:00",
                "timeClose": "2000-01-01T16:15:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T14:00:00-05:00",
                "timeClose": "2000-01-01T16:15:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T14:00:00-05:00",
                "timeClose": "2000-01-01T16:15:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b6fe5894-ed50-ee11-9935-000d3a55a2f5",
        "name": "On The Go Services - Cleveland",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Cleveland, OH",
        "description": None,
        "metaDescription": "Visit PrintScan in Cleveland, Ohio for exceptional Live Scan and Fingerprinting services. Our skilled team delivers quick and accurate results, fulfilling all your identification needs. Depend on PrintScan Cleveland for your secure and efficient fingerprinting requirements.",
        "notes": "Visit PrintScan in Cleveland, Ohio for exceptional Live Scan and Fingerprinting services. Our skilled team delivers quick and accurate results, fulfilling all your identification needs. Depend on PrintScan Cleveland for your secure and efficient fingerprinting requirements.",
        "address1": "15728 Lorain Rd",
        "address2": None,
        "stateCountry": "OH",
        "city": "Cleveland",
        "postalCode": "44111",
        "county": "Cuyahoga",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.809050,
        "latitude": 41.451829,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T12:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "3abfe839-ef50-ee11-9935-000d3a55a2f5",
        "name": "Maxrox LLC DBA A+ Mailboxes & More LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - San Francisco, CA",
        "description": None,
        "metaDescription": "Discover PrintScan in San Francisco, California, a leading provider of high-quality Live Scan and Fingerprinting services. Experience our fast, secure, and reliable solutions tailored to your needs today.",
        "notes": "Discover PrintScan in San Francisco, California, a leading provider of high-quality Live Scan and Fingerprinting services. Experience our fast, secure, and reliable solutions tailored to your needs today.",
        "address1": "3041 Mission Street",
        "address2": None,
        "stateCountry": "CA",
        "city": "San Francisco",
        "postalCode": "94110",
        "county": "San Francisco",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -122.417828,
        "latitude": 37.748533,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-09-15T10:15:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-15T17:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-09-15T10:15:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-15T17:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-09-15T10:15:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-15T17:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-09-15T10:15:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-15T17:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-09-15T10:15:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-15T17:30:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-09-15T10:15:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-15T16:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "64d92a10-1453-ee11-9935-000d3a55a2f5",
        "name": "Rogue Valley Mail + More LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Eagle Point, OR",
        "description": None,
        "metaDescription": "Discover PrintScan in Eagle Point, Oregon, your trusted destination for high-quality Live Scan and Fingerprinting services. Experience fast, secure, and reliable fingerprinting solutions with PrintScan Eagle Point today.",
        "notes": "Discover PrintScan in Eagle Point, Oregon, your trusted destination for high-quality Live Scan and Fingerprinting services. Experience fast, secure, and reliable fingerprinting solutions with PrintScan Eagle Point today.",
        "address1": "10558 Highway 62",
        "address2": "Suite B1",
        "stateCountry": "OR",
        "city": "Eagle Point",
        "postalCode": "97524",
        "county": "Jackson",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -122.813244,
        "latitude": 42.464735,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-09-14T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-14T17:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-09-14T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-14T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-09-14T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-14T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-09-14T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-14T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-09-14T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-14T17:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-09-14T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-14T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "91249de7-1453-ee11-9935-000d3a55a2f5",
        "name": "Postal Connections",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Boise, ID",
        "description": None,
        "metaDescription": "Choose PrintScan in Boise, Idaho for all your Live Scan and Fingerprinting needs. We offer secure, efficient, and accurate identity verification services, ensuring your peace of mind and satisfaction.",
        "notes": "Choose PrintScan in Boise, Idaho for all your Live Scan and Fingerprinting needs. We offer secure, efficient, and accurate identity verification services, ensuring your peace of mind and satisfaction.",
        "address1": "10673 West Lake Hazel Rd",
        "address2": None,
        "stateCountry": "ID",
        "city": "Boise",
        "postalCode": "83709",
        "county": "Ada",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -116.314883,
        "latitude": 43.546164,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-09-14T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-14T13:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "92249de7-1453-ee11-9935-000d3a55a2f5",
        "name": "Columbus Testing LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Whiteville, NC",
        "description": None,
        "metaDescription": "Experience fast and reliable Live Scan and Fingerprinting services at PrintScan in Whiteville, North Carolina. Our certified professionals ensure accurate results for all your identification needs.",
        "notes": "Experience fast and reliable Live Scan and Fingerprinting services at PrintScan in Whiteville, North Carolina. Our certified professionals ensure accurate results for all your identification needs.",
        "address1": "108B Memory Plaza",
        "address2": None,
        "stateCountry": "NC",
        "city": "Whiteville",
        "postalCode": "28472",
        "county": "Columbus",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -78.704357,
        "latitude": 34.339305,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "2b223176-3d53-ee11-9935-000d3a55a2f5",
        "name": "Wesley Chapel Fingerprinting Services LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Wesley Chapel, FL",
        "description": None,
        "metaDescription": "Discover top-tier Live Scan and Fingerprinting services at PrintScan in Wesley Chapel, Florida. We prioritize accuracy and efficiency in meeting all your identification requirements.",
        "notes": "Discover top-tier Live Scan and Fingerprinting services at PrintScan in Wesley Chapel, Florida. We prioritize accuracy and efficiency in meeting all your identification requirements.",
        "address1": "28210 Paseo Drive Building 190",
        "address2": "Suite 104",
        "stateCountry": "FL",
        "city": "Wesley Chapel",
        "postalCode": "33543",
        "county": "Hillsborough",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -82.349682,
        "latitude": 28.188170,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T19:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T19:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T19:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T19:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "1982d92b-6ca1-ed11-994d-00224826a175",
        "name": "Essential Support Services LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Eldersburg, MD",
        "description": None,
        "metaDescription": "Choose PrintScan in Eldersburg, Maryland for superior Live Scan and Fingerprinting services. Our dedicated team delivers precise and prompt results for all your identification needs.",
        "notes": "Choose PrintScan in Eldersburg, Maryland for superior Live Scan and Fingerprinting services. Our dedicated team delivers precise and prompt results for all your identification needs.",
        "address1": "2028 Liberty Road",
        "address2": "Suite 102",
        "stateCountry": "MD",
        "city": "Eldersburg",
        "postalCode": "21784",
        "county": "Carroll",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -76.922959,
        "latitude": 39.397618,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-01-31T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-01-31T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-01-31T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-01-31T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-01-31T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-01-31T19:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-01-31T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-01-31T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-01-31T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-01-31T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "cbf7acf7-e9a6-ed11-994d-00224826a175",
        "name": "GMMC & Aesthetics (GM Medical Consultants)",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Coral Springs, FL",
        "description": "In Omega One Building (Second Floor), Between Chipotle and MedExpress",
        "metaDescription": "Experience superior Live Scan and Fingerprinting services at PrintScan in Coral Springs, Florida. Choose PrintScan for your secure, fast, and precise scanning solutions.",
        "notes": "Experience superior Live Scan and Fingerprinting services at PrintScan in Coral Springs, Florida. Choose PrintScan for your secure, fast, and precise scanning solutions.",
        "address1": "1801 N. University Dr.",
        "address2": "Suite 206",
        "stateCountry": "FL",
        "city": "Coral Springs",
        "postalCode": "33071",
        "county": "Broward",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.252214,
        "latitude": 26.253073,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-07T15:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-07T15:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-07T15:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-07T15:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-07T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "0daab95e-b6a7-ed11-994d-00224826a175",
        "name": "Indiana Firearms",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Lebanon, IN",
        "description": None,
        "metaDescription": "Choose PrintScan in Lebanon, Indiana for dependable Live Scan and Fingerprinting services. Our dedicated team delivers accurate and fast results, meeting all your identification requirements efficiently.",
        "notes": "Choose PrintScan in Lebanon, Indiana for dependable Live Scan and Fingerprinting services. Our dedicated team delivers accurate and fast results, meeting all your identification requirements efficiently.",
        "address1": "2354 N. Lebanon St.",
        "address2": None,
        "stateCountry": "IN",
        "city": "Lebanon",
        "postalCode": "46052",
        "county": "Boone",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -86.475042,
        "latitude": 40.068084,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-07-21T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-21T17:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-21T17:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-07-21T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-21T17:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-07-21T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-21T17:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-07-21T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-21T17:30:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-07-21T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-21T15:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "906a4b64-0e5a-ed11-819b-00224826ab24",
        "name": "Alliance 2020 of Seattle LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Seattle Kiosk Location",
        "description": None,
        "metaDescription": "Explore PrintScan in Seattle, Washington, the leading provider of Live Scan and Fingerprinting services. Offering efficient, accurate, and secure identification solutions to cater to your specific requirements.",
        "notes": "Explore PrintScan in Seattle, Washington, the leading provider of Live Scan and Fingerprinting services. Offering efficient, accurate, and secure identification solutions to cater to your specific requirements.",
        "address1": "2033 6th Avenue",
        "address2": "Suite 901",
        "stateCountry": "WA",
        "city": "Seattle",
        "postalCode": "98121",
        "county": "King",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -122.339194,
        "latitude": 47.614592,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2022-11-11T08:30:00+00:00",
                "timeLunch": "2022-11-11T12:00:00+00:00",
                "timeResume": "2022-11-11T13:00:00+00:00",
                "timeClose": "2022-11-11T16:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2022-11-11T08:30:00+00:00",
                "timeLunch": "2022-11-11T12:00:00+00:00",
                "timeResume": "2022-11-11T13:00:00+00:00",
                "timeClose": "2022-11-11T16:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2022-11-11T08:30:00+00:00",
                "timeLunch": "2022-11-11T12:00:00+00:00",
                "timeResume": "2022-11-11T13:00:00+00:00",
                "timeClose": "2022-11-11T16:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2022-11-11T08:30:00+00:00",
                "timeLunch": "2022-11-11T12:00:00+00:00",
                "timeResume": "2022-11-11T13:00:00+00:00",
                "timeClose": "2022-11-11T16:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2022-11-11T08:30:00+00:00",
                "timeLunch": "2022-11-11T12:00:00+00:00",
                "timeResume": "2022-11-11T13:00:00+00:00",
                "timeClose": "2022-11-11T16:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "3165234a-855b-ed11-819b-00224826ab24",
        "name": "Covenant Lab Services",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Tampa, FL",
        "description": "Building 300",
        "metaDescription": "Visit PrintScan in Tampa, Florida, your go-to source for professional Live Scan and Fingerprinting services. Experience our quick, secure, and trustworthy fingerprinting solutions at PrintScan Tampa today.",
        "notes": "Visit PrintScan in Tampa, Florida, your go-to source for professional Live Scan and Fingerprinting services. Experience our quick, secure, and trustworthy fingerprinting solutions at PrintScan Tampa today.",
        "address1": "7402 North 56th Street",
        "address2": "Suite 355",
        "stateCountry": "FL",
        "city": "Tampa",
        "postalCode": "33617",
        "county": "Hillsborough",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -82.395271,
        "latitude": 28.014572,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": "2000-01-01T13:00:00-04:00",
                "timeResume": "2000-01-01T14:00:00-04:00",
                "timeClose": "2000-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": "2000-01-01T13:00:00-04:00",
                "timeResume": "2000-01-01T14:00:00-04:00",
                "timeClose": "2000-01-01T18:30:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": "2000-01-01T13:00:00-04:00",
                "timeResume": "2000-01-01T14:00:00-04:00",
                "timeClose": "2000-01-01T18:30:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": "2000-01-01T13:00:00-04:00",
                "timeResume": "2000-01-01T14:00:00-04:00",
                "timeClose": "2000-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": "2000-01-01T13:00:00-04:00",
                "timeResume": "2000-01-01T14:00:00-04:00",
                "timeClose": "2000-01-01T17:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "176aead4-0465-ed11-819b-00224826ab24",
        "name": "SHIKA365 LLC  DBA: WESHIP",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - St. Petersburg, FL",
        "description": None,
        "metaDescription": "Experience superior Live Scan and Fingerprinting services at PrintScan in Saint Petersburg, Florida. Providing swift, dependable, and professional solutions for all your identity verification needs. Rely on PrintScan Saint Petersburg, FL - Your local expert in Live Scan and Fingerprinting technology.",
        "notes": "Experience superior Live Scan and Fingerprinting services at PrintScan in Saint Petersburg, Florida. Providing swift, dependable, and professional solutions for all your identity verification needs. Rely on PrintScan Saint Petersburg, FL - Your local expert in Live Scan and Fingerprinting technology.",
        "address1": "1128 94th Avenue N",
        "address2": None,
        "stateCountry": "FL",
        "city": "Saint Petersburg",
        "postalCode": "33702",
        "county": "Pinellas",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -82.649383,
        "latitude": 27.856872,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:30:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:30:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:30:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": "2000-01-01T12:30:00-04:00",
                "timeResume": "2000-01-01T13:30:00-04:00",
                "timeClose": "2000-01-01T18:30:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:30:00-04:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T10:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:30:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "30747d31-666b-ed11-819b-00224826ab24",
        "name": "Optimus Multi-Services LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center",
        "description": None,
        "metaDescription": "Discover PrintScan in Naples, Florida, your trusted destination for efficient Live Scan and Fingerprinting services. Experience our fast, accurate, and reliable solutions today!",
        "notes": "Discover PrintScan in Naples, Florida, your trusted destination for efficient Live Scan and Fingerprinting services. Experience our fast, accurate, and reliable solutions today!",
        "address1": "7795 Davis Blvd",
        "address2": "Ste 205",
        "stateCountry": "FL",
        "city": "Naples",
        "postalCode": "34104",
        "county": "Collier",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.710714,
        "latitude": 26.139643,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-06-05T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-05T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-06-05T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-05T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-06-05T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-05T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-06-05T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-05T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-06-05T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-05T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "c7a15cd9-e882-ed11-9d7a-00224826ad2f",
        "name": "Florida Bail Bonds Association, Inc.",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Miami Gardens",
        "description": None,
        "metaDescription": "Choose PrintScan in Miami Gardens, Florida for superior Live Scan and Fingerprinting services. We are dedicated to providing accurate and efficient identification solutions for your security needs.",
        "notes": "Choose PrintScan in Miami Gardens, Florida for superior Live Scan and Fingerprinting services. We are dedicated to providing accurate and efficient identification solutions for your security needs.",
        "address1": "260 NW 183rd street",
        "address2": None,
        "stateCountry": "FL",
        "city": "Miami Gardens",
        "postalCode": "33169",
        "county": "Miami-Dade",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.206683,
        "latitude": 25.942202,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2022-12-23T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-12-23T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2022-12-23T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-12-23T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2022-12-23T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-12-23T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-04-20T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-20T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-04-20T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-20T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "7afa1be0-7a8b-ed11-9d7a-00224826ad2f",
        "name": "Garden State Administrative Solutions",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Hammonton, NJ",
        "description": "Located in the Augusta Complex - Weekends by Appointment Only",
        "metaDescription": "Experience top-notch Live Scan and Fingerprinting services at PrintScan in Hammonton, New Jersey. We're dedicated to providing reliable, efficient identification solutions to meet your unique needs.",
        "notes": "Experience top-notch Live Scan and Fingerprinting services at PrintScan in Hammonton, New Jersey. We're dedicated to providing reliable, efficient identification solutions to meet your unique needs.",
        "address1": "858 S White Horse Pike",
        "address2": "Suite 8",
        "stateCountry": "NJ",
        "city": "Hammonton",
        "postalCode": "08037",
        "county": "Atlantic",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -74.774792,
        "latitude": 39.620515,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-31T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-31T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-31T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-31T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-31T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "d6d65790-2091-ed11-9d7a-00224826ad2f",
        "name": "DWS Mobile Notary and Fingerprinting LLC.",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Phenix City, AL",
        "description": "PLEASE NOTE: There is no ADA Access to this office",
        "metaDescription": "Choose PrintScan in Phenix City, Alabama for high-quality Live Scan and Fingerprinting services. We are committed to delivering accurate and fast identification solutions for your peace of mind.",
        "notes": "Choose PrintScan in Phenix City, Alabama for high-quality Live Scan and Fingerprinting services. We are committed to delivering accurate and fast identification solutions for your peace of mind.",
        "address1": "1617 Broad St",
        "address2": None,
        "stateCountry": "AL",
        "city": "Phenix City",
        "postalCode": "36867",
        "county": "Lee",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -85.001236,
        "latitude": 32.475744,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-07-24T09:00:00+00:00",
                "timeLunch": "2023-07-24T13:00:00+00:00",
                "timeResume": "2023-07-24T14:00:00+00:00",
                "timeClose": "2023-07-24T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-05-15T09:00:00+00:00",
                "timeLunch": "2023-05-15T13:00:00+00:00",
                "timeResume": "2023-05-15T14:00:00+00:00",
                "timeClose": "2023-05-15T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-05-15T09:00:00+00:00",
                "timeLunch": "2023-05-15T13:00:00+00:00",
                "timeResume": "2023-05-15T14:00:00+00:00",
                "timeClose": "2023-05-15T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "3b2c2cd9-8a79-450f-93a6-00d298dddab4",
        "name": "YMCA DENVER (Open Tues)",
        "displayName": "PrintScan | YMCA DENVER (Open Tues) - Denver, CO",
        "description": "YMCA DENVER",
        "metaDescription": "Experience fast and reliable Live Scan and Fingerprinting services in Denver, Colorado with PrintScan. Trust our experts for secure, high-quality, and efficient fingerprinting solutions.",
        "notes": "Experience fast and reliable Live Scan and Fingerprinting services in Denver, Colorado with PrintScan. Trust our experts for secure, high-quality, and efficient fingerprinting solutions.",
        "address1": "2625 S Colorado Blvd",
        "address2": None,
        "stateCountry": "CO",
        "city": "Denver",
        "postalCode": "80222",
        "county": "Denver",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.941349,
        "latitude": 39.669096,
        "googlePlaceId": None,
        "referenceId": "72",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "8c6a730d-3510-4888-8a28-08db145b7857",
        "name": "Colorado Fingerprinting Downtown (Open M-F)",
        "displayName": "PrintScan | Colorado Fingerprinting Downtown (Open M-F) - Denver, CO",
        "description": "Petroleum Building Southern End of 16th St Mall on the 8th Floor",
        "metaDescription": "Discover PrintScan in Denver, Colorado, your trusted destination for Live Scan and Fingerprinting services. Experience our fast, reliable, and secure solutions tailored to meet your individual needs.",
        "notes": "Discover PrintScan in Denver, Colorado, your trusted destination for Live Scan and Fingerprinting services. Experience our fast, reliable, and secure solutions tailored to meet your individual needs.",
        "address1": "110 16th St Mall",
        "address2": None,
        "stateCountry": "CO",
        "city": "Denver",
        "postalCode": "80202",
        "county": "Denver",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.987763,
        "latitude": 39.741452,
        "googlePlaceId": None,
        "referenceId": "46",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "d7ef472e-aa3a-495d-f4f7-08dc1c2b1491",
        "name": "AKIR Enterprises LLC dba Akir Screening Solutions",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Five Points, AL",
        "description": None,
        "metaDescription": "Explore PrintScan in Five Points, Alabama, your reliable source for advanced Live Scan and Fingerprinting services. Benefit from our precise, secure, and efficient solutions tailored to meet your identification requirements.",
        "notes": "Explore PrintScan in Five Points, Alabama, your reliable source for advanced Live Scan and Fingerprinting services. Benefit from our precise, secure, and efficient solutions tailored to meet your identification requirements.",
        "address1": "28175 US Hwy 431",
        "address2": None,
        "stateCountry": "AL",
        "city": "Five Points",
        "postalCode": "36855",
        "county": "Chambers",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -85.348480,
        "latitude": 33.037860,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T10:00:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-06:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:00:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-06:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:00:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-06:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:00:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-06:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-06:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "a912f3a6-f792-4764-31d1-08dc1c480065",
        "name": "LUX Diagnostics LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Henderson, NC",
        "description": None,
        "metaDescription": "Visit PrintScan in Henderson, North Carolina, your go-to provider for top-notch Live Scan and Fingerprinting services. Enjoy our secure, fast, and accurate identification solutions designed to cater to your specific needs.",
        "notes": "Visit PrintScan in Henderson, North Carolina, your go-to provider for top-notch Live Scan and Fingerprinting services. Enjoy our secure, fast, and accurate identification solutions designed to cater to your specific needs.",
        "address1": "1695 Parham Street",
        "address2": None,
        "stateCountry": "NC",
        "city": "Henderson",
        "postalCode": "27536",
        "county": "Vance",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -78.423234,
        "latitude": 36.326633,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "18a91bbb-5d18-497a-31d4-08dc1c480065",
        "name": "Fastest Labs of Richmond",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Richmond, CA",
        "description": None,
        "metaDescription": "Discover PrintScan in Richmond, California - your trusted destination for high-quality Live Scan and Fingerprinting services. Experience fast, secure, and reliable solutions tailored to meet your identification needs.",
        "notes": "Discover PrintScan in Richmond, California - your trusted destination for high-quality Live Scan and Fingerprinting services. Experience fast, secure, and reliable solutions tailored to meet your identification needs.",
        "address1": "4261 A Hilltop Drive",
        "address2": None,
        "stateCountry": "CA",
        "city": "Richmond",
        "postalCode": "94803",
        "county": "Contra Costa",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -122.312546,
        "latitude": 37.976738,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T10:00:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-08:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:00:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-08:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:00:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-08:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:00:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-08:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-08:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "0bef4235-2bc5-4fc1-52ce-08dc27fd6a19",
        "name": "Alamo Brass LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Garden Ridge, TX",
        "description": None,
        "metaDescription": "Explore PrintScan in Garden Ridge, Texas, your trusted provider for exceptional Live Scan and Fingerprinting services. Experience our accurate, fast, and dependable solutions, designed to cater to your unique needs.",
        "notes": "Explore PrintScan in Garden Ridge, Texas, your trusted provider for exceptional Live Scan and Fingerprinting services. Experience our accurate, fast, and dependable solutions, designed to cater to your unique needs.",
        "address1": "18838 FM 2252 BUILDING 600",
        "address2": None,
        "stateCountry": "TX",
        "city": "Garden Ridge",
        "postalCode": "78266",
        "county": "Comal",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -98.313998,
        "latitude": 29.615400,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T13:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "e9dbf4f6-472c-469a-97b2-08dc2da3ca77",
        "name": "Haute Screening and Wellness Zone",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Searcy, AR",
        "description": None,
        "metaDescription": "Discover PrintScan in Searcy, Arkansas, your trusted destination for high-quality Live Scan and Fingerprinting services. Ensure your security with our advanced technology and experienced team.",
        "notes": "Discover PrintScan in Searcy, Arkansas, your trusted destination for high-quality Live Scan and Fingerprinting services. Ensure your security with our advanced technology and experienced team.",
        "address1": "2705 E Moore Avenue",
        "address2": None,
        "stateCountry": "AR",
        "city": "Searcy",
        "postalCode": "72143",
        "county": "White",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -91.705220,
        "latitude": 35.253613,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-06:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-06:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-06:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-06:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-06:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "ab422e65-acf7-4b4b-97b5-08dc2da3ca77",
        "name": "DXP SERVICES Inc.",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Brooklyn, NY",
        "description": None,
        "metaDescription": "Discover PrintScan in Brooklyn, New York, your trusted destination for Live Scan and Fingerprinting services. Experience our fast, reliable, and secure solutions today.",
        "notes": "Discover PrintScan in Brooklyn, New York, your trusted destination for Live Scan and Fingerprinting services. Experience our fast, reliable, and secure solutions today.",
        "address1": "9 Lake Street",
        "address2": None,
        "stateCountry": "NY",
        "city": "Brooklyn",
        "postalCode": "11223",
        "county": "Kings",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -73.972865,
        "latitude": 40.603934,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "d0a5adde-6cbd-4829-909f-08dc331223f0",
        "name": "Express Ship and Pack ",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Deland, FL",
        "description": None,
        "metaDescription": "Explore PrintScan in Deland, Florida, your go-to source for Live Scan and Fingerprinting needs. Benefit from our quick, dependable, and safe services today.",
        "notes": "Explore PrintScan in Deland, Florida, your go-to source for Live Scan and Fingerprinting needs. Benefit from our quick, dependable, and safe services today.",
        "address1": "320 S. Spring Garden Avenue",
        "address2": "Suite E",
        "stateCountry": "FL",
        "city": "Deland",
        "postalCode": "32720",
        "county": "Lake",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.324534,
        "latitude": 29.024072,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T13:30:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b937e85a-0f70-481b-90a6-08dc331223f0",
        "name": "Fastest Labs of Chandler-Gilbert",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Chandler, AZ",
        "description": None,
        "metaDescription": "Visit PrintScan in Chandler, Arizona, your go-to source for Live Scan and Fingerprinting needs. Take advantage of our swift, reliable, and secure services today.",
        "notes": "Visit PrintScan in Chandler, Arizona, your go-to source for Live Scan and Fingerprinting needs. Take advantage of our swift, reliable, and secure services today.",
        "address1": "3120 N Arizona Avenue",
        "address2": "Suite 104",
        "stateCountry": "AZ",
        "city": "Chandler",
        "postalCode": "85225",
        "county": "Maricopa",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -111.842822,
        "latitude": 33.351866,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "4c723e6a-6225-4e93-4487-08dc36e68ba0",
        "name": "New Phase",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Indianapolis, IN",
        "description": "Inside of Lady J's Florist",
        "metaDescription": "Visit PrintScan in Indianapolis, Indiana, your go-to provider for superior Live Scan and Fingerprinting services. Leverage our high-tech systems for accurate and speedy results.",
        "notes": "Visit PrintScan in Indianapolis, Indiana, your go-to provider for superior Live Scan and Fingerprinting services. Leverage our high-tech systems for accurate and speedy results.",
        "address1": "2060 N. Illinois St.",
        "address2": None,
        "stateCountry": "IN",
        "city": "Indianapolis",
        "postalCode": "46202",
        "county": "Marion",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -86.093771,
        "latitude": 39.748205,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T19:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "515f9c6a-4a11-45ba-4489-08dc36e68ba0",
        "name": "T & T Shooters Supply ",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Yakima, WA",
        "description": None,
        "metaDescription": "Choose PrintScan in Yakima, Washington, your top-notch provider for professional Live Scan and Fingerprinting services. Take advantage of our innovative technology for exact and swift outcomes.",
        "notes": "Choose PrintScan in Yakima, Washington, your top-notch provider for professional Live Scan and Fingerprinting services. Take advantage of our innovative technology for exact and swift outcomes.",
        "address1": "308 N 6th Avenue",
        "address2": None,
        "stateCountry": "WA",
        "city": "Yakima",
        "postalCode": "98902",
        "county": "Yakima",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -120.519739,
        "latitude": 46.604140,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T11:00:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-08:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T11:00:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-08:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T11:00:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-08:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T11:00:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-08:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T11:00:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-08:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T10:00:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-08:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "5249d0f2-ffaf-47ad-dc57-08dc38790c66",
        "name": "Sticks R Us LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Rosedale, MD",
        "description": None,
        "metaDescription": "Select PrintScan in Rosedale, Maryland, your dependable choice for top-quality Live Scan and Fingerprinting services. Trust our state-of-the-art technology for accurate and fast results.",
        "notes": "Select PrintScan in Rosedale, Maryland, your dependable choice for top-quality Live Scan and Fingerprinting services. Trust our state-of-the-art technology for accurate and fast results.",
        "address1": "9106 Philadelphia Road",
        "address2": "Suite 106",
        "stateCountry": "MD",
        "city": "Rosedale",
        "postalCode": "21237",
        "county": "Baltimore",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -76.473525,
        "latitude": 39.347482,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 0,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T13:00:00-05:00"
            },
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T13:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "a26f3d77-1e3e-41ce-374b-08dc39bd4b19",
        "name": "Test ABI Location 0809",
        "displayName": "PrintScan | Test ABI Location 0809 - Denver, CO",
        "description": "New Location created on 08/09",
        "metaDescription": "Choose PrintScan in Aurora, Colorado, your reliable choice for exceptional Live Scan and Fingerprinting services. Take advantage of our speedy, secure, and dependable fingerprinting offerings at PrintScan today.",
        "notes": "Choose PrintScan in Aurora, Colorado, your reliable choice for exceptional Live Scan and Fingerprinting services. Take advantage of our speedy, secure, and dependable fingerprinting offerings at PrintScan today.",
        "address1": "110 16th St Mall",
        "address2": None,
        "stateCountry": "CO",
        "city": "Denver",
        "postalCode": "80202",
        "county": "Adams",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.987763,
        "latitude": 39.741452,
        "googlePlaceId": None,
        "referenceId": "147",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "a3bfa25d-a42c-4002-bbda-08dc3fae1adb",
        "name": "CMB Consultancy LLC (New Jersey)",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Bayonne, NJ",
        "description": None,
        "metaDescription": "Discover PrintScan in Bayonne, New Jersey, your trusted destination for efficient Live Scan and Fingerprinting services. Experience our high-quality, secure, and fast solutions today.",
        "notes": "Discover PrintScan in Bayonne, New Jersey, your trusted destination for efficient Live Scan and Fingerprinting services. Experience our high-quality, secure, and fast solutions today.",
        "address1": "473 Broadway",
        "address2": "Suite 403",
        "stateCountry": "NJ",
        "city": "Bayonne",
        "postalCode": "07002",
        "county": "Hudson",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -74.119155,
        "latitude": 40.663441,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "8b8be5a7-5ec1-47ad-d1b5-08dc443b20df",
        "name": "Citywide Protection Services",
        "displayName": "PrintScan Authorized Fingerprint Service Center- Chesapeake, VA",
        "description": None,
        "metaDescription": "Visit PrintScan in Chesapeake, Virginia, your trusted center for professional Live Scan and Fingerprinting services. Benefit from our secure, speedy, and high-grade solutions now.",
        "notes": "Visit PrintScan in Chesapeake, Virginia, your trusted center for professional Live Scan and Fingerprinting services. Benefit from our secure, speedy, and high-grade solutions now.",
        "address1": "1403 Greenbriar Pkwy",
        "address2": "Suite 440",
        "stateCountry": "VA",
        "city": "Chesapeake",
        "postalCode": "23320",
        "county": "Chesapeake City",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -76.228811,
        "latitude": 36.775582,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "24e2dc54-2cf2-4e65-257e-08dc4a9ed8fc",
        "name": "Favorable Behavior Support Services LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Indianapolis, IN",
        "description": None,
        "metaDescription": "Explore PrintScan in Indianapolis, Indiana, your reliable source for Live Scan and Fingerprinting services. Enjoy our efficient, precise, and confidential processing today!",
        "notes": "Explore PrintScan in Indianapolis, Indiana, your reliable source for Live Scan and Fingerprinting services. Enjoy our efficient, precise, and confidential processing today!",
        "address1": "7210 Madison Avenue",
        "address2": "Suite H",
        "stateCountry": "IN",
        "city": "Indianapolis",
        "postalCode": "46227",
        "county": "Marion",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -86.127042,
        "latitude": 39.662499,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": "2000-01-01T14:00:00-04:00",
                "timeResume": "2000-01-01T15:00:00-04:00",
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": "2000-01-01T14:00:00-04:00",
                "timeResume": "2000-01-01T15:00:00-04:00",
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": "2000-01-01T14:00:00-04:00",
                "timeResume": "2000-01-01T15:00:00-04:00",
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": "2000-01-01T14:00:00-04:00",
                "timeResume": "2000-01-01T15:00:00-04:00",
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": "2000-01-01T14:00:00-04:00",
                "timeResume": "2000-01-01T15:00:00-04:00",
                "timeClose": "2000-01-01T17:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "7d0245bc-3c8f-4ade-3138-08dc4da69e8d",
        "name": "The UPS Store 5722",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Savannah, GA",
        "description": None,
        "metaDescription": "Visit PrintScan in Savannah, Georgia for top-tier Live Scan and Fingerprinting services. Benefit from our rapid, precise, and confidential processing solutions today!",
        "notes": "Visit PrintScan in Savannah, Georgia for top-tier Live Scan and Fingerprinting services. Benefit from our rapid, precise, and confidential processing solutions today!",
        "address1": "5710 Ogeechee Road",
        "address2": "Suite 200",
        "stateCountry": "GA",
        "city": "Savannah",
        "postalCode": "31405",
        "county": "Chatham",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.225686,
        "latitude": 32.026213,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "aef1d309-f5bf-49fb-9c1a-08dc7e230cb4",
        "name": "Accurate Biometrics - Itasca",
        "displayName": "PrintScan | Accurate Biometrics - Itasca - Itasca, IL",
        "description": None,
        "metaDescription": None,
        "notes": None,
        "address1": "500 Park Blvd",
        "address2": "Suite 1260",
        "stateCountry": "IL",
        "city": "Itasca",
        "postalCode": "60143",
        "county": "Dupage",
        "phone": "",
        "email": "",
        "longitude": -88.017894,
        "latitude": 41.986665,
        "googlePlaceId": None,
        "referenceId": "ABHQ",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "e8342644-6de1-4fff-9c1b-08dc7e230cb4",
        "name": "The UPS Store 0051",
        "displayName": "PrintScan | UPS Store 0051 - SAN FRANCISCO, CA",
        "description": None,
        "metaDescription": None,
        "notes": None,
        "address1": "1819 POLK ST",
        "address2": "",
        "stateCountry": "CA",
        "city": "SAN FRANCISCO",
        "postalCode": "94109",
        "county": "San Francisco",
        "phone": "(415)441-4954",
        "email": "store0051@theupsstore.com",
        "longitude": -122.421465,
        "latitude": 37.793669,
        "googlePlaceId": None,
        "referenceId": "TUPSS0051",
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 0,
                "timeOpen": "2024-05-27T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-05-27T16:00:00+00:00"
            },
            {
                "dayOfWeek": 1,
                "timeOpen": "2024-05-27T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-05-27T19:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2024-05-27T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-05-27T19:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2024-05-27T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-05-27T19:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2024-05-27T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-05-27T19:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2024-05-27T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-05-27T19:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2024-05-27T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2024-05-27T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "ef31afe8-993e-4f88-b838-08dc9236976b",
        "name": "Center Police Station (Open Wed & Thurs)",
        "displayName": "PrintScan | Center Police Station (Open Wed & Thurs) - Center, CO",
        "description": "",
        "metaDescription": None,
        "notes": None,
        "address1": "294 S Worth St",
        "address2": None,
        "stateCountry": "CO",
        "city": "Center",
        "postalCode": "81125",
        "county": "Saguache",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -106.108105,
        "latitude": 37.753590,
        "googlePlaceId": None,
        "referenceId": "8",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "2ac066a2-64ae-41e3-b839-08dc9236976b",
        "name": "Alaska Location",
        "displayName": "PrintScan | Alaska Location - Unalaska, AK",
        "description": "HAST Time",
        "metaDescription": None,
        "notes": None,
        "address1": "2716 Airport Beach Rd",
        "address2": None,
        "stateCountry": "AK",
        "city": "Unalaska",
        "postalCode": "99692",
        "county": "Aleutians West",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -166.540162,
        "latitude": 53.894669,
        "googlePlaceId": None,
        "referenceId": "148",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "52446a8c-74ed-40d4-b83a-08dc9236976b",
        "name": "Test Alaska Location",
        "displayName": "PrintScan | Test Alaska Location - Anchorage, AK",
        "description": "Alaska Location",
        "metaDescription": None,
        "notes": None,
        "address1": "4700 Union Square Dr",
        "address2": None,
        "stateCountry": "AK",
        "city": "Anchorage",
        "postalCode": "99503",
        "county": "Anchorage",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -149.884851,
        "latitude": 61.177842,
        "googlePlaceId": None,
        "referenceId": "149",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "e207f75d-81a8-450a-b83b-08dc9236976b",
        "name": "Sahil locations_place1",
        "displayName": "PrintScan | Sahil locations_place1 - Potter, KS",
        "description": "Demo test location",
        "metaDescription": None,
        "notes": None,
        "address1": "66002",
        "address2": None,
        "stateCountry": "KS",
        "city": "Potter",
        "postalCode": "66002",
        "county": "Atchison",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -95.141913,
        "latitude": 39.425831,
        "googlePlaceId": None,
        "referenceId": "152",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "6bd2e67f-48cc-44de-b83c-08dc9236976b",
        "name": "Sahillocation_1990",
        "displayName": "PrintScan | Sahillocation_1990 - Palm Desert, CA",
        "description": "Fingerprint Location_1990",
        "metaDescription": None,
        "notes": None,
        "address1": "76676 Hollyhock Dr",
        "address2": None,
        "stateCountry": "CA",
        "city": "Palm Desert",
        "postalCode": "92211",
        "county": "Riverside",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -116.326766,
        "latitude": 33.758804,
        "googlePlaceId": None,
        "referenceId": "154",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "02d38a7a-70f9-4f66-b83d-08dc9236976b",
        "name": "SahilNewtestlocation_1",
        "displayName": "PrintScan | SahilNewtestlocation_1 - Miami, FL",
        "description": "",
        "metaDescription": None,
        "notes": None,
        "address1": "8765 S Dixie Hwy",
        "address2": None,
        "stateCountry": "FL",
        "city": "Miami",
        "postalCode": "33143",
        "county": "Miami-Dade",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.307064,
        "latitude": 25.689307,
        "googlePlaceId": None,
        "referenceId": "156",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "ca29a6b5-d24d-4d0b-b83e-08dc9236976b",
        "name": "PawanLocation",
        "displayName": "PrintScan | PawanLocation - Murrieta, CA",
        "description": "PawanLocation",
        "metaDescription": None,
        "notes": None,
        "address1": "41139 Marseille Ct",
        "address2": None,
        "stateCountry": "CA",
        "city": "Murrieta",
        "postalCode": "92562",
        "county": "Riverside",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -117.214726,
        "latitude": 33.573273,
        "googlePlaceId": None,
        "referenceId": "157",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "af444674-42bb-4fe1-4c39-08dcc6cf4839",
        "name": "LightRegression 126 -> Location ",
        "displayName": "NewClient Location Light Regression126",
        "description": "Description",
        "metaDescription": None,
        "notes": "<p>PrintScan understands the confidential nature of your fingerprint data, and we value your privacy. You can be assured that whatever your fingerprinting purpose, whether it’s an FBI background check, an ATF fingerprinting, or an apostille, your information is safe with us.<br></p>",
        "address1": "1 Long Island Ave",
        "address2": "Suite11",
        "stateCountry": "NY",
        "city": "Farmingdale",
        "postalCode": "11735",
        "county": "Nassau",
        "phone": "+16317821700",
        "email": "kathy@printscan.com",
        "longitude": -73.386390,
        "latitude": 40.747060,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "656bf73c-f425-49dc-4627-08dcd0e8673f",
        "name": "LabCorp - Denver",
        "displayName": "LabCorp - Denver",
        "description": "Use to test merger of LabCorp",
        "metaDescription": None,
        "notes": "<p>PrintScan understands the confidential nature of your fingerprint data, and we value your privacy. You can be assured that whatever your fingerprinting purpose, whether it’s an FBI background check, an ATF fingerprinting, or an apostille, your information is safe with us.<br></p>",
        "address1": "3333 Regis Blvd",
        "address2": None,
        "stateCountry": "CO",
        "city": "Denver",
        "postalCode": "80221",
        "county": "Denver",
        "phone": None,
        "email": None,
        "longitude": -105.033917,
        "latitude": 39.789084,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b2f780a9-86a9-4f7e-961c-12a3ef2548f1",
        "name": "Inbox & More Pack Ship Print",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Bannockburn, IL",
        "description": None,
        "metaDescription": "Explore PrintScan Bannockburn, Illinois, the leading provider of Live Scan and Fingerprinting services. We offer precise, reliable, and confidential solutions tailored to your identification requirements.",
        "notes": "Explore PrintScan Bannockburn, Illinois, the leading provider of Live Scan and Fingerprinting services. We offer precise, reliable, and confidential solutions tailored to your identification requirements.",
        "address1": "2515 Waukegan Road",
        "address2": None,
        "stateCountry": "IL",
        "city": "Bannockburn",
        "postalCode": "60015",
        "county": "Lake",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -87.859550,
        "latitude": 42.197825,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:00:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-06:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-06:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-06:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-06:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-06:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T09:00:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-06:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "767d3dd6-4f40-4255-a6b2-15bc7ab8d32b",
        "name": "Ouray Public Library (Open Wednesdays)",
        "displayName": "PrintScan | Ouray Public Library (Open Wednesdays) - Ouray, CO",
        "description": "",
        "metaDescription": "Discover PrintScan in Ouray, Colorado, your trusted destination for top-notch Live Scan and Fingerprinting services. Experience quick, accurate, and reliable solutions for all your identification needs.",
        "notes": "Discover PrintScan in Ouray, Colorado, your trusted destination for top-notch Live Scan and Fingerprinting services. Experience quick, accurate, and reliable solutions for all your identification needs.",
        "address1": "320 6th Ave",
        "address2": None,
        "stateCountry": "CO",
        "city": "Ouray",
        "postalCode": "81427",
        "county": "Ouray",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -107.670458,
        "latitude": 38.023036,
        "googlePlaceId": None,
        "referenceId": "126",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "9248a463-2a21-4862-8475-15ed4b834171",
        "name": "Demand Drug and Background Screening LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Euclid, OH",
        "description": "Located in Demand Drug and Background Screening LLC.",
        "metaDescription": "Discover PrintScan in Euclid, Ohio, your trusted destination for efficient Live Scan and Fingerprinting services. Experience our state-of-the-art technology for accurate and reliable results.",
        "notes": "Discover PrintScan in Euclid, Ohio, your trusted destination for efficient Live Scan and Fingerprinting services. Experience our state-of-the-art technology for accurate and reliable results.",
        "address1": "761 East 200th St.",
        "address2": None,
        "stateCountry": "OH",
        "city": "Euclid",
        "postalCode": "44119",
        "county": "Cuyahoga",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.539531,
        "latitude": 41.585685,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b3fb35e0-6a9c-40e7-9d52-17a918d8b2fa",
        "name": "Limon Memorial Library (Open Mon-Fri)",
        "displayName": "PrintScan | Limon Memorial Library (Open Mon-Fri) - Limon, CO",
        "description": "",
        "metaDescription": "Explore PrintScan in Limon, Colorado, your premier choice for efficient Live Scan and Fingerprinting services. We offer fast, precise, and dependable solutions tailored to meet your identification requirements.",
        "notes": "Explore PrintScan in Limon, Colorado, your premier choice for efficient Live Scan and Fingerprinting services. We offer fast, precise, and dependable solutions tailored to meet your identification requirements.",
        "address1": "205 E Ave",
        "address2": None,
        "stateCountry": "CO",
        "city": "Limon",
        "postalCode": "80828",
        "county": "Lincoln",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -103.688078,
        "latitude": 39.262055,
        "googlePlaceId": None,
        "referenceId": "50",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "9d16c8c2-56c3-47a9-aabf-1d5e81c0f5eb",
        "name": "Montrose County Sheriff (Open Mon-Fri)",
        "displayName": "PrintScan | Montrose County Sheriff (Open Mon-Fri) - Montrose, CO",
        "description": "Go Left from the Main Entrance and follow the \"Blue Line\" to the back Visitor Entrance",
        "metaDescription": "Welcome to PrintScan in Montrose, Colorado, your go-to source for professional Live Scan and Fingerprinting services. We provide swift, accurate, and reliable identification solutions to cater to your specific needs.",
        "notes": "Welcome to PrintScan in Montrose, Colorado, your go-to source for professional Live Scan and Fingerprinting services. We provide swift, accurate, and reliable identification solutions to cater to your specific needs.",
        "address1": "1200 N Grand Ave",
        "address2": None,
        "stateCountry": "CO",
        "city": "Montrose",
        "postalCode": "81401",
        "county": "Montrose",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -107.890877,
        "latitude": 38.487630,
        "googlePlaceId": None,
        "referenceId": "104",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "77448d6f-b292-455c-b31a-1d9c5ddfdfb4",
        "name": "High Valley Community Center Del Norte (Open Tues-Thurs)",
        "displayName": "PrintScan | High Valley Community Center Del Norte (Open Tues-Thurs) - Del Norte, CO",
        "description": "",
        "metaDescription": "Visit PrintScan in Del Norte, Colorado, your reliable provider for high-quality Live Scan and Fingerprinting services. Benefit from our fast, precise, and trustworthy identification solutions designed to suit your individual needs.",
        "notes": "Visit PrintScan in Del Norte, Colorado, your reliable provider for high-quality Live Scan and Fingerprinting services. Benefit from our fast, precise, and trustworthy identification solutions designed to suit your individual needs.",
        "address1": "595 Grand Ave",
        "address2": None,
        "stateCountry": "CO",
        "city": "Del Norte",
        "postalCode": "81132",
        "county": "Rio Grande",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -106.354979,
        "latitude": 37.678663,
        "googlePlaceId": None,
        "referenceId": "16",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "e5daa469-001d-4d37-a9ca-20ca62e8c572",
        "name": "ARCPoint Labs of Marysville-Arlington",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Arlington, WA",
        "description": None,
        "metaDescription": "Welcome to PrintScan Arlington, Washington - your go-to source for Live Scan and Fingerprinting services. Experience our efficient, trustworthy, and secure solutions, customized to fulfill your individual needs.",
        "notes": "Welcome to PrintScan Arlington, Washington - your go-to source for Live Scan and Fingerprinting services. Experience our efficient, trustworthy, and secure solutions, customized to fulfill your individual needs.",
        "address1": "17306 Smokey Point Drive",
        "address2": "Suite 21",
        "stateCountry": "WA",
        "city": "Arlington",
        "postalCode": "98223",
        "county": "Snohomish",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -122.187269,
        "latitude": 48.153415,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:30:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-08:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:30:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-08:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:30:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-08:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:30:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-08:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:30:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-08:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "0c1889b5-6c21-4479-9041-212668953e37",
        "name": "KCG Drug Alcohol S'olutions (\"Open Mon-Fr)",
        "displayName": "PrintScan | KCG Drug Alcohol S'olutions (\"Open Mon-Fr) - Westminster, CO",
        "description": "Enter t'hrough the Left Side of \"Building B\" and access Ste 107",
        "metaDescription": "Rely on PrintScan in Arvada, Colorado for exceptional Live Scan and Fingerprinting services. We prioritize security and efficiency, providing high-quality fingerprinting solutions for your needs.",
        "notes": "Rely on PrintScan in Arvada, Colorado for exceptional Live Scan and Fingerprinting services. We prioritize security and efficiency, providing high-quality fingerprinting solutions for your needs.",
        "address1": "80003",
        "address2": None,
        "stateCountry": "CO",
        "city": "Westminster",
        "postalCode": "80003",
        "county": "Jefferson",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -105.067432,
        "latitude": 39.818249,
        "googlePlaceId": None,
        "referenceId": "115",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "93829b54-9e45-492c-a430-236d0c17e020",
        "name": "Maggies Shipping Shoppe Colorado Springs (Open Mon-Fri)",
        "displayName": "PrintScan | Maggies Shipping Shoppe Colorado Springs (Open Mon-Fri) - Colorado Springs, CO",
        "description": "",
        "metaDescription": "Explore PrintScan in Colorado Springs, Colorado, your go-to source for fast and reliable Live Scan and Fingerprinting services. Benefit from our cutting-edge technology for precise results every time.",
        "notes": "Explore PrintScan in Colorado Springs, Colorado, your go-to source for fast and reliable Live Scan and Fingerprinting services. Benefit from our cutting-edge technology for precise results every time.",
        "address1": "330 E Costilla St",
        "address2": None,
        "stateCountry": "CO",
        "city": "Colorado Springs",
        "postalCode": "80903",
        "county": "El Paso",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.818664,
        "latitude": 38.828351,
        "googlePlaceId": None,
        "referenceId": "11",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "60076f1e-7718-4d5c-9cf7-25732f49c25c",
        "name": "Colorado Mobile Drug Testing Denver (Open Mon-Fri)",
        "displayName": "PrintScan | Colorado Mobile Drug Testing Denver (Open Mon-Fri) - Denver, CO",
        "description": "",
        "metaDescription": "Experience the best in Live Scan and Fingerprinting services with PrintScan in Denver, Colorado. We provide secure, efficient, and high-quality fingerprinting solutions tailored to your needs.",
        "notes": "Experience the best in Live Scan and Fingerprinting services with PrintScan in Denver, Colorado. We provide secure, efficient, and high-quality fingerprinting solutions tailored to your needs.",
        "address1": "18300 E 71st Ave Ste. 135",
        "address2": None,
        "stateCountry": "CO",
        "city": "Denver",
        "postalCode": "80249",
        "county": "Denver",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.773781,
        "latitude": 39.825063,
        "googlePlaceId": None,
        "referenceId": "17",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b40649cf-6933-ec11-9820-281878546d6b",
        "name": "Echelon Artistry's LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Fountain Hills",
        "description": None,
        "metaDescription": "Discover superior Live Scan and Fingerprinting services at PrintScan in Fountain Hills, Arizona. Our expert team ensures swift and precise results, fulfilling all your identification requirements with utmost accuracy. Choose PrintScan Fountain Hills for your secure and efficient fingerprinting needs.",
        "notes": "Discover superior Live Scan and Fingerprinting services at PrintScan in Fountain Hills, Arizona. Our expert team ensures swift and precise results, fulfilling all your identification requirements with utmost accuracy. Choose PrintScan Fountain Hills for your secure and efficient fingerprinting needs.",
        "address1": "13229 N Verde River Dr",
        "address2": "Suite 300",
        "stateCountry": "AZ",
        "city": "Fountain Hills",
        "postalCode": "85268",
        "county": "Maricopa",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -111.717042,
        "latitude": 33.606848,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-02-24T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-24T15:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-02-24T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-24T15:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-02-24T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-24T15:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-02-24T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-24T15:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-02-24T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-24T15:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-02-24T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-24T18:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "34d99216-bc35-ec11-9820-281878546d6b",
        "name": "Motary Notary Fingerprinting & More",
        "displayName": "PrintScan Authorized Fingerprint Service Center - North Charleston, SC",
        "description": "Motary Notary is located inside the Clekis Law Firm Building, but is not affiliated with The Clekis Law Firm",
        "metaDescription": "Experience top-tier Live Scan and Fingerprinting services at PrintScan in North Charleston, South Carolina. Our dedicated professionals deliver fast and accurate results, making us your go-to solution for all identification needs. Trust PrintScan North Charleston for secure and efficient fingerprinting processes.",
        "notes": "Experience top-tier Live Scan and Fingerprinting services at PrintScan in North Charleston, South Carolina. Our dedicated professionals deliver fast and accurate results, making us your go-to solution for all identification needs. Trust PrintScan North Charleston for secure and efficient fingerprinting processes.",
        "address1": "2850 Ashley Phosphate Road",
        "address2": "Suite F",
        "stateCountry": "SC",
        "city": "North Charleston",
        "postalCode": "29418",
        "county": "Charleston",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.056608,
        "latitude": 32.932132,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-02-14T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-14T15:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-02-14T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-14T15:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-02-14T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-14T15:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-02-14T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-14T15:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-02-14T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-14T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "45d208f6-6536-ec11-9820-281878546d6b",
        "name": "Vicom Ventures",
        "displayName": "PrintScan - Authorized Fingerprint Service Center",
        "description": None,
        "metaDescription": "Experience the best in Live Scan and Fingerprinting services with PrintScan in Denton, Texas. We are your local experts for secure and efficient identity verification.",
        "notes": "Experience the best in Live Scan and Fingerprinting services with PrintScan in Denton, Texas. We are your local experts for secure and efficient identity verification.",
        "address1": "3730 E Mckinney St",
        "address2": "STE 105, RM C",
        "stateCountry": "TX",
        "city": "Denton",
        "postalCode": "76208",
        "county": "Denton",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -97.088551,
        "latitude": 33.211578,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "72d19c17-e23b-ec11-9820-281878546d6b",
        "name": "The Mail Center",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Titusville, FL",
        "description": None,
        "metaDescription": "Visit PrintScan in Titusville, Florida, your leading provider for state-of-the-art Live Scan and Fingerprinting services. Benefit from our quick, secure, and trustworthy fingerprinting solutions at PrintScan Titusville today.",
        "notes": "Visit PrintScan in Titusville, Florida, your leading provider for state-of-the-art Live Scan and Fingerprinting services. Benefit from our quick, secure, and trustworthy fingerprinting solutions at PrintScan Titusville today.",
        "address1": "3206 S Hopkins Ave",
        "address2": None,
        "stateCountry": "FL",
        "city": "Titusville",
        "postalCode": "32780",
        "county": "Brevard",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.805271,
        "latitude": 28.579848,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-06-21T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-21T14:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-06-21T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-21T14:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-06-21T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-21T14:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-06-21T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-21T14:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-06-21T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-21T14:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "599c0b22-d836-4a43-aa73-293743a1b73e",
        "name": "One Source Drug Screening (Open M-F)",
        "displayName": "PrintScan | One Source Drug Screening (Open M-F) - Fort Collins, CO",
        "description": "Also known as Fastest Labs Drug Screening STE 102",
        "metaDescription": "Opt for PrintScan in Fort Collins, Colorado for unparalleled Live Scan and Fingerprinting services. We offer secure, efficient, and high-quality fingerprinting solutions to cater to your specific needs.",
        "notes": "Opt for PrintScan in Fort Collins, Colorado for unparalleled Live Scan and Fingerprinting services. We offer secure, efficient, and high-quality fingerprinting solutions to cater to your specific needs.",
        "address1": "1040 E Elizabeth St",
        "address2": None,
        "stateCountry": "CO",
        "city": "Fort Collins",
        "postalCode": "80524",
        "county": "Larimer",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -105.058710,
        "latitude": 40.574520,
        "googlePlaceId": None,
        "referenceId": "137",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "d07cf607-6f76-46d5-8818-322408fa1b43",
        "name": "Colorado Fingerprinting The Center (Open Wednesdays)",
        "displayName": "PrintScan | Colorado Fingerprinting The Center (Open Wednesdays) - Denver, CO",
        "description": "",
        "metaDescription": "Choose PrintScan in Denver, Colorado, your trusted partner for comprehensive Live Scan and Fingerprinting services. We ensure quick, precise, and reliable identification solutions to meet your specific needs.",
        "notes": "Choose PrintScan in Denver, Colorado, your trusted partner for comprehensive Live Scan and Fingerprinting services. We ensure quick, precise, and reliable identification solutions to meet your specific needs.",
        "address1": "1301 E Colfax Ave",
        "address2": None,
        "stateCountry": "CO",
        "city": "Denver",
        "postalCode": "80218",
        "county": "Denver",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.970419,
        "latitude": 39.740267,
        "googlePlaceId": None,
        "referenceId": "61",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "f363b9a3-4dbd-4724-88f2-36456551b386",
        "name": "Walden (Open Tues & Wed)",
        "displayName": "PrintScan | Walden (Open Tues & Wed) - Walden, CO",
        "description": "North Park School District Admin",
        "metaDescription": "Discover PrintScan in Walden, Colorado, your top choice for superior Live Scan and Fingerprinting services. We provide fast, precise, and trustworthy identification solutions to cater to your specific requirements.",
        "notes": "Discover PrintScan in Walden, Colorado, your top choice for superior Live Scan and Fingerprinting services. We provide fast, precise, and trustworthy identification solutions to cater to your specific requirements.",
        "address1": "910 4th St",
        "address2": None,
        "stateCountry": "CO",
        "city": "Walden",
        "postalCode": "80480",
        "county": "Jackson",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -106.277144,
        "latitude": 40.732344,
        "googlePlaceId": None,
        "referenceId": "124",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "eba2d58f-813d-4bc8-be71-37b8726e546e",
        "name": "Eagle Ship & Print LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Yerington, NV",
        "description": None,
        "metaDescription": "Get access to superior Live Scan and Fingerprinting services at PrintScan in Yerington, Nevada. We are committed to providing precise and swift identification services. Rely on PrintScan Yerington for all your fingerprinting needs.",
        "notes": "Get access to superior Live Scan and Fingerprinting services at PrintScan in Yerington, Nevada. We are committed to providing precise and swift identification services. Rely on PrintScan Yerington for all your fingerprinting needs.",
        "address1": "512 W. Goldfield Avenue",
        "address2": None,
        "stateCountry": "NV",
        "city": "Yerington",
        "postalCode": "89447",
        "county": "Lyon",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -119.169467,
        "latitude": 38.994244,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-07:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-07:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-07:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-07:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-07:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T09:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-07:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "5e1397b5-9a6f-4856-b685-37c7e8e6bbc1",
        "name": "Mail Boxes Buena Vista (Open Tues & Wed)",
        "displayName": "PrintScan | Mail Boxes Buena Vista (Open Tues & Wed) - Buena Vista, CO",
        "description": "STE A",
        "metaDescription": "Visit PrintScan in Buena Vista, Colorado, your reliable source for premium Live Scan and Fingerprinting services. We offer swift, accurate, and secure identification solutions tailored to your individual needs.",
        "notes": "Visit PrintScan in Buena Vista, Colorado, your reliable source for premium Live Scan and Fingerprinting services. We offer swift, accurate, and secure identification solutions tailored to your individual needs.",
        "address1": "29805 US-24 ste a",
        "address2": None,
        "stateCountry": "CO",
        "city": "Buena Vista",
        "postalCode": "81211",
        "county": "Chaffee",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -106.139570,
        "latitude": 38.852358,
        "googlePlaceId": None,
        "referenceId": "5",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "e48da4fc-111d-496d-ac28-389d4bf65ea9",
        "name": "Big Brothers Big Sisters Englewood (Open Tuesdays)",
        "displayName": "PrintScan | Big Brothers Big Sisters Englewood (Open Tuesdays) - Englewood, CO",
        "description": "Go to the 4th floor suite 450",
        "metaDescription": "Explore PrintScan in Englewood, Colorado, your dependable hub for Live Scan and Fingerprinting services. Enjoy our quick, reliable, and tailored solutions designed to accommodate your specific needs.",
        "notes": "Explore PrintScan in Englewood, Colorado, your dependable hub for Live Scan and Fingerprinting services. Enjoy our quick, reliable, and tailored solutions designed to accommodate your specific needs.",
        "address1": "750 W Hampden Ave #450",
        "address2": None,
        "stateCountry": "CO",
        "city": "Englewood",
        "postalCode": "80110",
        "county": "Arapahoe",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.996416,
        "latitude": 39.652436,
        "googlePlaceId": None,
        "referenceId": "18",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "2d04c3ec-fa74-4313-87ad-395fe0f44731",
        "name": "KCG Drug Alcohol Solutions Evergreen (Open Mon-Tues)",
        "displayName": "PrintScan | KCG Drug Alcohol Solutions Evergreen (Open Mon-Tues) - Evergreen, CO",
        "description": "Suite 100",
        "metaDescription": "Welcome to PrintScan in Evergreen, Colorado, your trusted destination for high-quality Live Scan and Fingerprinting services. Experience our quick, precise, and reliable identification solutions designed to meet your specific needs.",
        "notes": "Welcome to PrintScan in Evergreen, Colorado, your trusted destination for high-quality Live Scan and Fingerprinting services. Experience our quick, precise, and reliable identification solutions designed to meet your specific needs.",
        "address1": "28577 S Buffalo Park Rd Suite 100",
        "address2": None,
        "stateCountry": "CO",
        "city": "Evergreen",
        "postalCode": "80439",
        "county": "Clear Creek",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -105.325546,
        "latitude": 39.625048,
        "googlePlaceId": None,
        "referenceId": "19",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "8d1a227b-6ff0-4eff-a637-3bfca5de224d",
        "name": "Colorado Fingerprinting Koelbel Library (Open Mon, Tues & Thurs)",
        "displayName": "PrintScan | Colorado Fingerprinting Koelbel Library (Open Mon, Tues & Thurs) - Centennial, CO",
        "description": "Check-in at Main Entrance Reception",
        "metaDescription": "Discover PrintScan in Centennial, Colorado, your top choice for Live Scan and Fingerprinting services. Experience our fast, secure, and customized solutions that are designed to suit your individual needs.",
        "notes": "Discover PrintScan in Centennial, Colorado, your top choice for Live Scan and Fingerprinting services. Experience our fast, secure, and customized solutions that are designed to suit your individual needs.",
        "address1": "5955 S Holly St",
        "address2": None,
        "stateCountry": "CO",
        "city": "Centennial",
        "postalCode": "80121",
        "county": "Arapahoe",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.923644,
        "latitude": 39.608949,
        "googlePlaceId": None,
        "referenceId": "53",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b1c8dbce-13d8-4b23-bfe3-3cf04eb93782",
        "name": "Life Bloom Labs  ",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Mooresville, NC",
        "description": "Directly across from the National Guard Armory. It will be the last office, next to a pit-stop. DOOR STAY LOCKED. PLEASE FOLLOW STEPS ON DOOR.",
        "metaDescription": "Explore PrintScan in Mooresville, North Carolina, your premier choice for efficient Live Scan and Fingerprinting services. We provide fast, accurate, and dependable identification solutions tailored to your unique requirements.",
        "notes": "Explore PrintScan in Mooresville, North Carolina, your premier choice for efficient Live Scan and Fingerprinting services. We provide fast, accurate, and dependable identification solutions tailored to your unique requirements.",
        "address1": "710 N Broad Street",
        "address2": "Suite 13",
        "stateCountry": "NC",
        "city": "Mooresville",
        "postalCode": "28115",
        "county": "Rowan",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.809100,
        "latitude": 35.596712,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T19:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T19:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T19:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T19:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-05:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "345ef318-dd16-4964-b212-3fcde2c3b69e",
        "name": "Occupational Screening & Health Services",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Bowling Green, KY",
        "description": "Turn onto Pedigo Way from Scottsville rd. Red Lobster is across the rd. From where you turn on Pedigo Way. Go down a little way Then office complexes on left we are in Ste.",
        "metaDescription": "Visit PrintScan in Bowling Green, Kentucky, your premier choice for top-notch Live Scan and Fingerprinting services. Trust PrintScan for your secure, swift, and accurate scanning requirements.",
        "notes": "Visit PrintScan in Bowling Green, Kentucky, your premier choice for top-notch Live Scan and Fingerprinting services. Trust PrintScan for your secure, swift, and accurate scanning requirements.",
        "address1": "1043 Pedigo Way",
        "address2": None,
        "stateCountry": "KY",
        "city": "Bowling Green",
        "postalCode": "42103",
        "county": "Warren",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -86.422408,
        "latitude": 36.952480,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": "2000-01-01T11:30:00-05:00",
                "timeResume": "2000-01-01T12:30:00-05:00",
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": "2000-01-01T11:30:00-05:00",
                "timeResume": "2000-01-01T12:30:00-05:00",
                "timeClose": "2000-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": "2000-01-01T11:30:00-05:00",
                "timeResume": "2000-01-01T12:30:00-05:00",
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": "2000-01-01T11:30:00-05:00",
                "timeResume": "2000-01-01T12:30:00-05:00",
                "timeClose": "2000-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": "2000-01-01T11:30:00-05:00",
                "timeResume": "2000-01-01T12:30:00-05:00",
                "timeClose": "2000-01-01T16:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "f5eb3d2d-990a-44e5-bed4-45c67b2eb2c2",
        "name": "Colorado Fingerprinting Union Lakewood (Open Mon-Fri)",
        "displayName": "PrintScan | Colorado Fingerprinting Union Lakewood (Open Mon-Fri) - Lakewood, CO",
        "description": "Located with Regus Group 2nd floor suite 200, it is best to park in back (east parking lot) instead of in front.",
        "metaDescription": "Discover PrintScan in Lakewood, Colorado, your premier provider for Live Scan and Fingerprinting services. Take advantage of our efficient, secure, and tailored solutions designed to meet your unique needs.",
        "notes": "Discover PrintScan in Lakewood, Colorado, your premier provider for Live Scan and Fingerprinting services. Take advantage of our efficient, secure, and tailored solutions designed to meet your unique needs.",
        "address1": "Regus - Lakewood - 200 Union",
        "address2": None,
        "stateCountry": "CO",
        "city": "Lakewood",
        "postalCode": "80228",
        "county": "Jefferson",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -105.132000,
        "latitude": 39.718700,
        "googlePlaceId": None,
        "referenceId": "122",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "c53ac103-7a55-442f-ada9-46a8b0a07885",
        "name": "Rapid Ship Republic LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Republic, MO",
        "description": None,
        "metaDescription": "Experience the best in Live Scan and Fingerprinting services at PrintScan in Republic, Missouri. Our focus on precision and speed in identification services distinguishes us from the rest. Choose PrintScan Republic for all your fingerprinting requirements.",
        "notes": "Experience the best in Live Scan and Fingerprinting services at PrintScan in Republic, Missouri. Our focus on precision and speed in identification services distinguishes us from the rest. Choose PrintScan Republic for all your fingerprinting requirements.",
        "address1": "513 US Highway 60E",
        "address2": None,
        "stateCountry": "MO",
        "city": "Republic",
        "postalCode": "65738",
        "county": "Greene",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -93.472802,
        "latitude": 37.117315,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "e03776cc-b6a5-4355-9b85-4c63f1aa2004",
        "name": "Montrose Hilltop Family Resource Center (Open Mon-Thurs)",
        "displayName": "PrintScan | Montrose Hilltop Family Resource Center (Open Mon-Thurs) - Montrose, CO",
        "description": "",
        "metaDescription": "Experience PrintScan in Montrose, Colorado, your dependable provider for high-quality Live Scan and Fingerprinting services. Benefit from our fast, precise, and reliable identification solutions designed to suit your individual needs.",
        "notes": "Experience PrintScan in Montrose, Colorado, your dependable provider for high-quality Live Scan and Fingerprinting services. Benefit from our fast, precise, and reliable identification solutions designed to suit your individual needs.",
        "address1": "540 S 1st St",
        "address2": None,
        "stateCountry": "CO",
        "city": "Montrose",
        "postalCode": "81401",
        "county": "Montrose",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -107.873672,
        "latitude": 38.479797,
        "googlePlaceId": None,
        "referenceId": "74",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "3cf7db59-7f27-434c-8fb3-4f04c9b5dce0",
        "name": "More Ink for Less LLC dba Warrington Pack & Ship Business Center",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Pensacola, FL",
        "description": None,
        "metaDescription": "Explore PrintScan in Pensacola, Florida, the leading destination for advanced Live Scan and Fingerprinting services. We provide secure, swift, and trusted solutions, making us your preferred choice for all identification needs.",
        "notes": "Explore PrintScan in Pensacola, Florida, the leading destination for advanced Live Scan and Fingerprinting services. We provide secure, swift, and trusted solutions, making us your preferred choice for all identification needs.",
        "address1": "120 Chiefs Way",
        "address2": "Suite 1",
        "stateCountry": "FL",
        "city": "Pensacola",
        "postalCode": "32507",
        "county": "Escambia",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -87.276152,
        "latitude": 30.407729,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "f35b0315-0572-4d13-a2ad-5009abb531da",
        "name": "JTI Drug & Alcohol Testing & Mobile Jo (Open Tues-Wed & Sun)",
        "displayName": "PrintScan | JTI Drug & Alcohol Testing & Mobile Jo (Open Tues-Wed & Sun) - Durango, CO",
        "description": "Ste 212",
        "metaDescription": "Visit PrintScan in Durango, Colorado, your leading source for exceptional Live Scan and Fingerprinting services. We deliver swift, accurate, and trustworthy identification solutions to cater to your specific requirements.",
        "notes": "Visit PrintScan in Durango, Colorado, your leading source for exceptional Live Scan and Fingerprinting services. We deliver swift, accurate, and trustworthy identification solutions to cater to your specific requirements.",
        "address1": "862 Main Ave Suite 212",
        "address2": None,
        "stateCountry": "CO",
        "city": "Durango",
        "postalCode": "81301",
        "county": "La Plata",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -107.880563,
        "latitude": 37.273152,
        "googlePlaceId": None,
        "referenceId": "113",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "e82a6154-889c-4203-9884-513f44d98034",
        "name": "Framingham Shipping Company",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Framingham, MA",
        "description": None,
        "metaDescription": "Visit PrintScan in Framingham, Massachusetts for premier Live Scan and Fingerprinting services. Our commitment to providing fast and accurate identification services makes us a trusted choice. Rely on PrintScan Framingham for all your fingerprinting needs.",
        "notes": "Visit PrintScan in Framingham, Massachusetts for premier Live Scan and Fingerprinting services. Our commitment to providing fast and accurate identification services makes us a trusted choice. Rely on PrintScan Framingham for all your fingerprinting needs.",
        "address1": "1257 Worcestor Road",
        "address2": None,
        "stateCountry": "MA",
        "city": "Framingham",
        "postalCode": "01701",
        "county": "Middlesex",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -71.449495,
        "latitude": 42.298523,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T13:30:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "74457b4d-66e3-40cc-b76e-5145f4bbf7a9",
        "name": "Fastest Labs Arvada (Open M-F)",
        "displayName": "PrintScan | Fastest Labs Arvada (Open M-F) - Arvada, CO",
        "description": "Suite 200",
        "metaDescription": "Trust PrintScan in Arvada, Colorado for all your Live Scan and Fingerprinting requirements. We provide secure, efficient, and top-quality fingerprinting solutions, designed to meet your specific needs.",
        "notes": "Trust PrintScan in Arvada, Colorado for all your Live Scan and Fingerprinting requirements. We provide secure, efficient, and top-quality fingerprinting solutions, designed to meet your specific needs.",
        "address1": "8850 W 58th Ave #200",
        "address2": None,
        "stateCountry": "CO",
        "city": "Arvada",
        "postalCode": "80002",
        "county": "Jefferson",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -105.096341,
        "latitude": 39.801716,
        "googlePlaceId": None,
        "referenceId": "134",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "a2377438-0e04-4b19-b223-51d004af8663",
        "name": "Complete Check",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Middletown, OH",
        "description": "Tall white building, located across from Olive Garden",
        "metaDescription": "Visit PrintScan in Middletown, Ohio, your premier provider for top-notch Live Scan and Fingerprinting services. Benefit from our swift, secure, and reliable fingerprinting procedures at PrintScan Middletown today.",
        "notes": "Visit PrintScan in Middletown, Ohio, your premier provider for top-notch Live Scan and Fingerprinting services. Benefit from our swift, secure, and reliable fingerprinting procedures at PrintScan Middletown today.",
        "address1": "6730 Roosevelt Avenue Suite 305",
        "address2": None,
        "stateCountry": "OH",
        "city": "Middletown",
        "postalCode": "45005",
        "county": "Warren",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -84.332192,
        "latitude": 39.493394,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T13:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "16f28ac5-8de8-49ce-ad6d-522f52cba473",
        "name": "Colorado Springs Fingerprinting (Open Mon-Fri)",
        "displayName": "PrintScan | Colorado Springs Fingerprinting (Open Mon-Fri) - Colorado Springs, CO",
        "description": "Enter in The Mail Center",
        "metaDescription": "Experience superior Live Scan and Fingerprinting services with PrintScan in Colorado Springs, Colorado. We are committed to delivering secure, efficient, and high-quality fingerprinting solutions for your needs.",
        "notes": "Experience superior Live Scan and Fingerprinting services with PrintScan in Colorado Springs, Colorado. We are committed to delivering secure, efficient, and high-quality fingerprinting solutions for your needs.",
        "address1": "6547 N Academy Blvd",
        "address2": None,
        "stateCountry": "CO",
        "city": "Colorado Springs",
        "postalCode": "80918",
        "county": "El Paso",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.792822,
        "latitude": 38.926942,
        "googlePlaceId": None,
        "referenceId": "9",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "9d5a7ccf-f321-4e6e-9f1b-5644d2d013b0",
        "name": "Midtown Shipping Solutions",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Jonesboro, AR",
        "description": "Middle Suite in The Delta Commons",
        "metaDescription": "Experience PrintScan in Jonesboro, Arkansas, your premier provider for Live Scan and Fingerprinting services. Take advantage of our quick, precise, and secure processing methods today!",
        "notes": "Experience PrintScan in Jonesboro, Arkansas, your premier provider for Live Scan and Fingerprinting services. Take advantage of our quick, precise, and secure processing methods today!",
        "address1": "2821 Race Street",
        "address2": "Suite C",
        "stateCountry": "AR",
        "city": "Jonesboro",
        "postalCode": "72401",
        "county": "Craighead",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -90.672005,
        "latitude": 35.813556,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T13:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "88472c27-9dff-479e-9462-5f335db58fb1",
        "name": "Durango Parks & Recreation (Open Tues & Thurs)",
        "displayName": "PrintScan | Durango Parks & Recreation (Open Tues & Thurs) - Durango, CO",
        "description": "",
        "metaDescription": "Experience PrintScan in Durango, Colorado, your trusted partner for comprehensive Live Scan and Fingerprinting services. We ensure quick, precise, and reliable identification solutions to meet your specific needs.",
        "notes": "Experience PrintScan in Durango, Colorado, your trusted partner for comprehensive Live Scan and Fingerprinting services. We ensure quick, precise, and reliable identification solutions to meet your specific needs.",
        "address1": "2700 Main Ave",
        "address2": None,
        "stateCountry": "CO",
        "city": "Durango",
        "postalCode": "81301",
        "county": "La Plata",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -107.871837,
        "latitude": 37.294122,
        "googlePlaceId": None,
        "referenceId": "70",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "c132e249-6bad-ed11-994c-6045bdd372a5",
        "name": "ARCpoint Labs of Greenville, SC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Greenville Kiosk Location",
        "description": "Conveniently located just 1.7 miles off of I-85 (Exit 39) in the Highland Business Park, directly across from the Breakaway Honda dealership.",
        "metaDescription": "Discover PrintScan in Greenville, South Carolina, your trusted destination for Live Scan and Fingerprinting services. Experience our fast, reliable, and secure solutions today.",
        "notes": "Discover PrintScan in Greenville, South Carolina, your trusted destination for Live Scan and Fingerprinting services. Experience our fast, reliable, and secure solutions today.",
        "address1": "355 Woodruff Road",
        "address2": "Suite 403",
        "stateCountry": "SC",
        "city": "Greenville",
        "postalCode": "29607",
        "county": "Greenville",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -82.341320,
        "latitude": 34.834419,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-02-15T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-15T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-02-15T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-15T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-02-15T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-15T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-02-15T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-15T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-02-15T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-02-15T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "fa77f0f2-6bad-ed11-994c-6045bdd372a5",
        "name": "ARCpoint Labs of Charleston",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Charleston Kiosk Location",
        "description": "Conveniently located approximately 1 mile from Interstate 26 (Exit 206B) behind Trident Hospital.",
        "metaDescription": "Experience top-tier Live Scan and Fingerprinting services at PrintScan in North Charleston, South Carolina. Our dedicated professionals deliver fast and accurate results, making us your go-to solution for all identification needs. Trust PrintScan North Charleston for secure and efficient fingerprinting processes.",
        "notes": "Experience top-tier Live Scan and Fingerprinting services at PrintScan in North Charleston, South Carolina. Our dedicated professionals deliver fast and accurate results, making us your go-to solution for all identification needs. Trust PrintScan North Charleston for secure and efficient fingerprinting processes.",
        "address1": "2831 Tricom Street",
        "address2": "Unit B",
        "stateCountry": "SC",
        "city": "North Charleston",
        "postalCode": "29406",
        "county": "Charleston",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.069766,
        "latitude": 32.974305,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-03-03T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-03T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-03-03T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-03T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-03-03T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-03T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-03-03T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-03T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-03-03T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-03T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "48d6029d-18b2-ed11-994c-6045bdd372a5",
        "name": "Exquisite Notary Solutions",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Miami, FL",
        "description": None,
        "metaDescription": "Explore PrintScan in Miami, Florida, your premier choice for advanced Live Scan and Fingerprinting services. Benefit from our swift, secure, and dependable fingerprinting processes at PrintScan Miami today.",
        "notes": "Explore PrintScan in Miami, Florida, your premier choice for advanced Live Scan and Fingerprinting services. Benefit from our swift, secure, and dependable fingerprinting processes at PrintScan Miami today.",
        "address1": "20401 Northwest 2nd Avenue",
        "address2": "Suite 103A",
        "stateCountry": "FL",
        "city": "Miami",
        "postalCode": "33169",
        "county": "Miami-Dade",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.205393,
        "latitude": 25.963424,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T19:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T22:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T19:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T22:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T19:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T22:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T19:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T22:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T19:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T22:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "52ec35bf-3c1c-ee11-a9bb-6045bdd5812c",
        "name": "ARCpoint Labs of Braintree-Quincy",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Braintree, MA",
        "description": None,
        "metaDescription": "Discover PrintScan in Braintree, Massachusetts, your trusted destination for efficient Live Scan and Fingerprinting services. Join our satisfied customers and experience our secure, fast, and reliable solutions.",
        "notes": "Discover PrintScan in Braintree, Massachusetts, your trusted destination for efficient Live Scan and Fingerprinting services. Join our satisfied customers and experience our secure, fast, and reliable solutions.",
        "address1": "420 Washington",
        "address2": "Suite 100",
        "stateCountry": "MA",
        "city": "Braintree",
        "postalCode": "02184",
        "county": "Norfolk",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -71.002835,
        "latitude": 42.218383,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-09-07T09:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00-04:00",
                "timeResume": "2000-01-01T13:00:00-04:00",
                "timeClose": "2023-09-07T15:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-09-07T09:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00-04:00",
                "timeResume": "2000-01-01T13:00:00-04:00",
                "timeClose": "2023-09-07T15:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-09-07T09:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00-04:00",
                "timeResume": "2000-01-01T13:00:00-04:00",
                "timeClose": "2023-09-07T15:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-09-07T09:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00-04:00",
                "timeResume": "2000-01-01T13:00:00-04:00",
                "timeClose": "2023-09-07T15:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": "2000-01-01T12:00:00-04:00",
                "timeResume": "2000-01-01T13:00:00-04:00",
                "timeClose": "2000-01-01T15:30:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "a208a2ca-3d1c-ee11-a9bb-6045bdd5812c",
        "name": "Netgain Corporation",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Knoxville, TN",
        "description": None,
        "metaDescription": "Choose PrintScan in Knoxville, Tennessee for superior Live Scan and Fingerprinting services. We provide quick, secure, and dependable solutions, making us your go-to choice for all identification and verification needs.",
        "notes": "Choose PrintScan in Knoxville, Tennessee for superior Live Scan and Fingerprinting services. We provide quick, secure, and dependable solutions, making us your go-to choice for all identification and verification needs.",
        "address1": "4605 Papermill Dr",
        "address2": None,
        "stateCountry": "TN",
        "city": "Knoxville",
        "postalCode": "37909",
        "county": "Knox",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -83.988187,
        "latitude": 35.951075,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-07-06T08:00:00+00:00",
                "timeLunch": "2023-07-06T12:00:00+00:00",
                "timeResume": "2023-07-06T13:00:00+00:00",
                "timeClose": "2023-07-06T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-07-06T08:00:00+00:00",
                "timeLunch": "2023-07-06T12:00:00+00:00",
                "timeResume": "2023-07-06T13:00:00+00:00",
                "timeClose": "2023-07-06T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-07-06T08:00:00+00:00",
                "timeLunch": "2023-07-06T12:00:00+00:00",
                "timeResume": "2023-07-06T13:00:00+00:00",
                "timeClose": "2023-07-06T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-07-06T08:00:00+00:00",
                "timeLunch": "2023-07-06T12:00:00+00:00",
                "timeResume": "2023-07-06T13:00:00+00:00",
                "timeClose": "2023-07-06T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-07-06T08:00:00+00:00",
                "timeLunch": "2023-07-06T12:00:00+00:00",
                "timeResume": "2023-07-06T13:00:00+00:00",
                "timeClose": "2023-07-06T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "3d20dc85-e71c-ee11-a9bb-6045bdd5812c",
        "name": "ARCpoint Labs of Chester",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Chester, VA",
        "description": "Across from the old Well's Fargo bank",
        "metaDescription": "Choose PrintScan in Chester, Virginia for all your Live Scan and Fingerprinting needs. Our dedicated team delivers high-quality, efficient identification services you can trust.",
        "notes": "Choose PrintScan in Chester, Virginia for all your Live Scan and Fingerprinting needs. Our dedicated team delivers high-quality, efficient identification services you can trust.",
        "address1": "13223 Rivers Bend Boulevard",
        "address2": None,
        "stateCountry": "VA",
        "city": "Chester",
        "postalCode": "23836",
        "county": "Chesterfield",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -77.356217,
        "latitude": 37.349860,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-27T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-27T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-27T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-27T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-27T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "d86ad876-f41c-ee11-a9bb-6045bdd5812c",
        "name": "Asset Acquisition Limited (Fastest Labs Englewood)",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Englewood, CO",
        "description": None,
        "metaDescription": "Choose PrintScan in Englewood, Colorado for fast, secure, and accurate Live Scan and Fingerprinting services. Our dedicated team is committed to providing top-notch identification solutions. Trust PrintScan Englewood, Colorado for all your identification needs.",
        "notes": "Choose PrintScan in Englewood, Colorado for fast, secure, and accurate Live Scan and Fingerprinting services. Our dedicated team is committed to providing top-notch identification solutions. Trust PrintScan Englewood, Colorado for all your identification needs.",
        "address1": "3601 S. Clarkson St.",
        "address2": "Suite 130",
        "stateCountry": "CO",
        "city": "Englewood",
        "postalCode": "80113",
        "county": "Arapahoe",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.978543,
        "latitude": 39.650450,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-30T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-30T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-30T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-30T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-30T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-30T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-30T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-30T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-30T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-30T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b583f1b2-7025-ee11-a9bb-6045bdd5812c",
        "name": "ARCpoint Labs of Salinas",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Salinas, CA",
        "description": None,
        "metaDescription": "Experience unparalleled Live Scan and Fingerprinting services at PrintScan in Salinas, California. Our state-of-the-art technology guarantees quick and accurate results. Rely on PrintScan Salinas for all your secure and efficient fingerprinting requirements.",
        "notes": "Experience unparalleled Live Scan and Fingerprinting services at PrintScan in Salinas, California. Our state-of-the-art technology guarantees quick and accurate results. Rely on PrintScan Salinas for all your secure and efficient fingerprinting requirements.",
        "address1": "635 Sanborn Pl",
        "address2": "Ste 24",
        "stateCountry": "CA",
        "city": "Salinas",
        "postalCode": "93901",
        "county": "Monterey",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -121.626750,
        "latitude": 36.665119,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-07-18T08:00:00+00:00",
                "timeLunch": "2023-07-18T11:30:00+00:00",
                "timeResume": "2023-07-18T14:00:00+00:00",
                "timeClose": "2023-07-18T15:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-07-18T08:00:00+00:00",
                "timeLunch": "2023-07-18T11:30:00+00:00",
                "timeResume": "2023-07-18T14:00:00+00:00",
                "timeClose": "2023-07-18T15:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-07-18T08:00:00+00:00",
                "timeLunch": "2023-07-18T11:30:00+00:00",
                "timeResume": "2023-07-18T14:00:00+00:00",
                "timeClose": "2023-07-18T15:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-07-18T08:00:00+00:00",
                "timeLunch": "2023-07-18T11:30:00+00:00",
                "timeResume": "2023-07-18T14:00:00+00:00",
                "timeClose": "2023-07-18T15:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-07-18T08:00:00+00:00",
                "timeLunch": "2023-07-18T11:30:00+00:00",
                "timeResume": "2023-07-18T14:00:00+00:00",
                "timeClose": "2023-07-18T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "ee87e09e-0c2b-ee11-b8f0-6045bdd58d5a",
        "name": "ABQ Fingerprinting",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Albuquerque, NM",
        "description": None,
        "metaDescription": "Welcome to PrintScan Albuquerque, New Mexico, your trusted source for Live Scan and Fingerprinting services. We provide swift, accurate, and secure identification solutions designed to meet your specific requirements.",
        "notes": "Welcome to PrintScan Albuquerque, New Mexico, your trusted source for Live Scan and Fingerprinting services. We provide swift, accurate, and secure identification solutions designed to meet your specific requirements.",
        "address1": "3620 Wyoming Blvd NE",
        "address2": "117",
        "stateCountry": "NM",
        "city": "Albuquerque",
        "postalCode": "87111",
        "county": "Bernalillo",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -106.550659,
        "latitude": 35.124442,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-03T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-03T16:45:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-03T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-03T16:45:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-03T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-03T16:45:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-03T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-03T16:45:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-03T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-03T16:45:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-08-03T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-03T12:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "4e2d528f-ae2b-ee11-b8f0-6045bdd58d5a",
        "name": "Mom and Pop Notary Shop LLC",
        "displayName": "Printscan Authorized Fingerprint Service Center - Phoenix, AZ",
        "description": None,
        "metaDescription": "Visit PrintScan in Phoenix, Arizona, your premier source for professional Live Scan and Fingerprinting services. Benefit from our fast, secure, and dependable fingerprinting systems at PrintScan Phoenix today.",
        "notes": "Visit PrintScan in Phoenix, Arizona, your premier source for professional Live Scan and Fingerprinting services. Benefit from our fast, secure, and dependable fingerprinting systems at PrintScan Phoenix today.",
        "address1": "3150 N 24th Street",
        "address2": "A100",
        "stateCountry": "AZ",
        "city": "Phoenix",
        "postalCode": "85016",
        "county": "Maricopa",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -112.030593,
        "latitude": 33.485292,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-31T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-31T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-31T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-31T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-31T13:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "c3bd1368-9f2c-ee11-b8f0-6045bdd58d5a",
        "name": "Healing Hands Lab",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Dunwoody, GA",
        "description": None,
        "metaDescription": "Choose PrintScan in Dunwoody, Georgia for superior Live Scan and Fingerprinting services. We offer secure, efficient, and accurate identification solutions to meet your unique needs.",
        "notes": "Choose PrintScan in Dunwoody, Georgia for superior Live Scan and Fingerprinting services. We offer secure, efficient, and accurate identification solutions to meet your unique needs.",
        "address1": "5 Dunwoody Park",
        "address2": "Suite 110",
        "stateCountry": "GA",
        "city": "Dunwoody",
        "postalCode": "30338",
        "county": "Dekalb",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -84.310112,
        "latitude": 33.923009,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-15T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-15T19:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-15T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-15T19:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-15T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-15T19:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-15T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-15T19:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-15T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-15T19:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-08-15T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-15T13:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "bb75d02b-a32c-ee11-b8f0-6045bdd58d5a",
        "name": "Giving Dream Inc",
        "displayName": "PrintScan Authorized Fingerprint Service Center - White Plains, NY",
        "description": "Ground Floor Office",
        "metaDescription": "Visit PrintScan in White Plains, New York for superior Live Scan and Fingerprinting services. We are dedicated to providing secure and accurate identity verification for your utmost convenience.",
        "notes": "Visit PrintScan in White Plains, New York for superior Live Scan and Fingerprinting services. We are dedicated to providing secure and accurate identity verification for your utmost convenience.",
        "address1": "202 Mamaroneck Avenue",
        "address2": "Suite 101",
        "stateCountry": "NY",
        "city": "White Plains",
        "postalCode": "10601",
        "county": "Westchester",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -73.764940,
        "latitude": 41.027877,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": "2000-01-01T13:00:00-04:00",
                "timeResume": "2000-01-01T14:00:00-04:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": "2000-01-01T13:00:00-04:00",
                "timeResume": "2000-01-01T14:00:00-04:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": "2000-01-01T13:00:00-04:00",
                "timeResume": "2000-01-01T14:00:00-04:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": "2000-01-01T13:00:00-04:00",
                "timeResume": "2000-01-01T14:00:00-04:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": "2000-01-01T13:00:00-04:00",
                "timeResume": "2000-01-01T14:00:00-04:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "23a8e171-a42c-ee11-b8f0-6045bdd58d5a",
        "name": "Ship Like That",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Clearwater, FL",
        "description": None,
        "metaDescription": "Visit PrintScan in Clearwater, Florida for exceptional Live Scan and Fingerprinting services. We are dedicated to delivering accurate and quick identification solutions for your convenience.",
        "notes": "Visit PrintScan in Clearwater, Florida for exceptional Live Scan and Fingerprinting services. We are dedicated to delivering accurate and quick identification solutions for your convenience.",
        "address1": "1444 S Belcher Rd",
        "address2": "Ste C",
        "stateCountry": "FL",
        "city": "Clearwater",
        "postalCode": "33764",
        "county": "Pinellas",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -82.746411,
        "latitude": 27.943893,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-22T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-22T18:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-22T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-22T18:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-22T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-22T18:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-22T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-22T18:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-22T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-22T18:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "8e7f4ba8-3032-ee11-b8f0-6045bdd58dec",
        "name": "Mr Tellers Mail Room LLC - DBA The Mail Room",
        "displayName": "PrintScan Authorized Fingerprint Service Center - University Pl, WA",
        "description": None,
        "metaDescription": "Opt for PrintScan in University Place, Washington for reliable Live Scan and Fingerprinting services. Our team is dedicated to providing accurate and swift results for all your identification needs.",
        "notes": "Opt for PrintScan in University Place, Washington for reliable Live Scan and Fingerprinting services. Our team is dedicated to providing accurate and swift results for all your identification needs.",
        "address1": "6824 19th St W",
        "address2": None,
        "stateCountry": "WA",
        "city": "University Place",
        "postalCode": "98466",
        "county": "Pierce",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -122.528877,
        "latitude": 47.241872,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-29T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T17:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-29T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T17:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-29T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T17:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-29T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T17:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-29T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T17:30:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-08-03T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-03T14:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "54a471b5-f432-ee11-b8f0-6045bdd58dec",
        "name": "Kimoz Consulting LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Woodbridge, VA",
        "description": "Right inside of brick-yard. Call or text upon arrival-#571-497-1148",
        "metaDescription": "Visit PrintScan in Woodbridge, Virginia for exceptional Live Scan and Fingerprinting services. Our dedicated team provides rapid and precise results for all your identification needs. Trust PrintScan Woodbridge for secure, efficient, and professional fingerprinting solutions.",
        "notes": "Visit PrintScan in Woodbridge, Virginia for exceptional Live Scan and Fingerprinting services. Our dedicated team provides rapid and precise results for all your identification needs. Trust PrintScan Woodbridge for secure, efficient, and professional fingerprinting solutions.",
        "address1": "2700 Neabsco Common Place",
        "address2": "Suite 101",
        "stateCountry": "VA",
        "city": "Woodbridge",
        "postalCode": "22191",
        "county": "Prince William",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -77.292257,
        "latitude": 38.623899,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T17:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T21:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T17:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T21:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T17:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T21:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T17:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T21:00:00-04:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-09-19T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-19T14:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "368fa350-0033-ee11-b8f0-6045bdd58dec",
        "name": "First Stop Medical Solutions",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Greensboro, NC",
        "description": None,
        "metaDescription": "Choose PrintScan in Greensboro, North Carolina for reliable Live Scan and Fingerprinting services. We are committed to providing innovative identification solutions for your safety and security.",
        "notes": "Choose PrintScan in Greensboro, North Carolina for reliable Live Scan and Fingerprinting services. We are committed to providing innovative identification solutions for your safety and security.",
        "address1": "5807 W. Gate City Blvd",
        "address2": None,
        "stateCountry": "NC",
        "city": "Greensboro",
        "postalCode": "27407",
        "county": "Guilford",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -79.897467,
        "latitude": 36.012748,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T10:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "d10f1570-f406-ee11-907c-6045bdd58e71",
        "name": "HO2 Systems LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Frisco, Texas",
        "description": None,
        "metaDescription": "Choose PrintScan in Frisco, Texas for superior Live Scan and Fingerprinting services. Our team is dedicated to providing precise and fast results, meeting all your identification requirements effectively.",
        "notes": "Choose PrintScan in Frisco, Texas for superior Live Scan and Fingerprinting services. Our team is dedicated to providing precise and fast results, meeting all your identification requirements effectively.",
        "address1": "4645 Avon Ln.",
        "address2": "Suite 220",
        "stateCountry": "TX",
        "city": "Frisco",
        "postalCode": "75033",
        "county": "Collin",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -96.846574,
        "latitude": 33.164694,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-06-22T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-22T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "0a738b90-fb06-ee11-907c-6045bdd58e71",
        "name": "ARCpoint Labs of Birmingham",
        "displayName": "PRINTSCAN AUTHORIZED FINGERPRINT SERVICE CENTER -Birmingham, AL",
        "description": "Greystone Centre next to Cowboys gas station in Greystone",
        "metaDescription": "Choose PrintScan in Birmingham, Alabama for reliable Live Scan and Fingerprinting services. Our commitment to advanced technology and professional service guarantees your security and convenience. Come see us today!",
        "notes": "Choose PrintScan in Birmingham, Alabama for reliable Live Scan and Fingerprinting services. Our commitment to advanced technology and professional service guarantees your security and convenience. Come see us today!",
        "address1": "5510 US-280",
        "address2": "Ste 215",
        "stateCountry": "AL",
        "city": "Birmingham",
        "postalCode": "35242",
        "county": "Shelby",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -86.664807,
        "latitude": 33.405873,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-06-09T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:45:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-06-09T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:45:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-06-09T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:45:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-06-09T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:45:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-06-09T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:45:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "0bb383a9-5c09-ee11-907c-6045bdd58e71",
        "name": "ARCpoint Labs of Austin North",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Austin, TX",
        "description": None,
        "metaDescription": "Visit PrintScan in Austin, Texas, your trusted source for high-quality Live Scan and Fingerprinting services. Experience our commitment to speed, security, and customer satisfaction today.",
        "notes": "Visit PrintScan in Austin, Texas, your trusted source for high-quality Live Scan and Fingerprinting services. Experience our commitment to speed, security, and customer satisfaction today.",
        "address1": "6448 E. Hwy 290",
        "address2": "Ste E105",
        "stateCountry": "TX",
        "city": "Austin",
        "postalCode": "78723",
        "county": "Travis",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -97.695931,
        "latitude": 30.322072,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "9eaa9937-f90a-ee11-907c-6045bdd58e71",
        "name": "Postnet",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Bakersfield, CA",
        "description": None,
        "metaDescription": "Discover top-notch Live Scan and Fingerprinting services at PrintScan in Bakersfield, California. We prioritize accuracy and efficiency in meeting all your identification requirements.",
        "notes": "Discover top-notch Live Scan and Fingerprinting services at PrintScan in Bakersfield, California. We prioritize accuracy and efficiency in meeting all your identification requirements.",
        "address1": "6077 Coffee Road",
        "address2": "Suite #4",
        "stateCountry": "CA",
        "city": "Bakersfield",
        "postalCode": "93308",
        "county": "Kern",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -119.091704,
        "latitude": 35.396897,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:30:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-07:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:30:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-07:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:30:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-07:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:30:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-07:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:30:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-07:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T09:00:00-08:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T13:45:00-08:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "a4d10d12-fc0a-ee11-907c-6045bdd58e71",
        "name": "StopNGo Notary",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Erie, PA",
        "description": None,
        "metaDescription": "Trust PrintScan in Erie, Pennsylvania for your Live Scan and Fingerprinting needs. We provide professional, efficient services for all your identification requirements.",
        "notes": "Trust PrintScan in Erie, Pennsylvania for your Live Scan and Fingerprinting needs. Located in StopNGo Wireless store. We provide professional, efficient services for all your identification requirements.",
        "address1": "732 Parade Street",
        "address2": None,
        "stateCountry": "PA",
        "city": "Erie",
        "postalCode": "16503",
        "county": "Erie",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.075864,
        "latitude": 42.130584,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-29T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T19:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-29T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T19:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-29T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T19:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-29T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T19:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-29T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T19:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-07-13T12:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-13T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "6cdebfc3-930b-ee11-907c-6045bdd58e71",
        "name": "ARCpoint Labs of Cedar Park",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Cedar Park, TX",
        "description": None,
        "metaDescription": "Turn to PrintScan in Cedar Park, Texas, for exceptional Live Scan and Fingerprinting services. Experience our dedication to providing fast, secure, and reliable solutions that meet your specific needs.",
        "notes": "Turn to PrintScan in Cedar Park, Texas, for exceptional Live Scan and Fingerprinting services. Experience our dedication to providing fast, secure, and reliable solutions that meet your specific needs.",
        "address1": "921 W New Hope Dr",
        "address2": "STE 103",
        "stateCountry": "TX",
        "city": "Cedar Park",
        "postalCode": "78613",
        "county": "Travis",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -97.846325,
        "latitude": 30.530103,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-06-17T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-17T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-06-17T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-17T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-06-17T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-17T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-06-17T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-17T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-06-17T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-17T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "897d0390-b40b-ee11-907c-6045bdd58e71",
        "name": "Peach Magnolia Notary & Fingerprinting",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Hiram, GA",
        "description": "Located in Building 2, behind AC Self Storage - Suite 19",
        "metaDescription": "Discover top-tier Live Scan and Fingerprinting services at PrintScan in Hiram, Georgia. Our professional team is committed to providing precise and efficient identification solutions. Choose PrintScan Hiram, GA for trusted and dependable service.",
        "notes": "Discover top-tier Live Scan and Fingerprinting services at PrintScan in Hiram, Georgia. Our professional team is committed to providing precise and efficient identification solutions. Choose PrintScan Hiram, GA for trusted and dependable service.",
        "address1": "5745 Wendy Bagwell Pkwy",
        "address2": "Suite 19",
        "stateCountry": "GA",
        "city": "Hiram",
        "postalCode": "30141",
        "county": "Paulding",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -84.732087,
        "latitude": 33.885700,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-06-20T09:30:00+00:00",
                "timeLunch": "2023-06-20T12:00:00+00:00",
                "timeResume": "2023-06-20T13:30:00+00:00",
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-06-20T09:30:00+00:00",
                "timeLunch": "2023-06-20T12:00:00+00:00",
                "timeResume": "2023-06-20T13:30:00+00:00",
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-06-20T09:30:00+00:00",
                "timeLunch": "2023-06-20T12:00:00+00:00",
                "timeResume": "2023-06-20T13:30:00+00:00",
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:30:00-04:00",
                "timeLunch": "2023-06-20T12:00:00+00:00",
                "timeResume": "2023-06-20T13:30:00+00:00",
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-06-20T09:30:00+00:00",
                "timeLunch": "2023-06-20T12:00:00+00:00",
                "timeResume": "2023-06-20T13:30:00+00:00",
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-06-20T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:30:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "37f391f3-350d-ee11-907c-6045bdd58e71",
        "name": "ARCpoint Labs of Philadelphia Central",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Philadelphia, PA",
        "description": "Entrance from 6th and Locust St, opposite Washington Park",
        "metaDescription": "Discover PrintScan in Philadelphia, Pennsylvania, your go-to source for exceptional Live Scan and Fingerprinting services. Experience our efficient, secure, and personalized identification solutions tailored to meet your specific needs.",
        "notes": "Discover PrintScan in Philadelphia, Pennsylvania, your go-to source for exceptional Live Scan and Fingerprinting services. Experience our efficient, secure, and personalized identification solutions tailored to meet your specific needs.",
        "address1": "233 S 6th St",
        "address2": "Suite C-2",
        "stateCountry": "PA",
        "city": "Philadelphia",
        "postalCode": "19106-3763",
        "county": "Philadelphia",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -75.150434,
        "latitude": 39.946143,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-06-17T09:00:00+00:00",
                "timeLunch": "2023-06-17T12:00:00+00:00",
                "timeResume": "2023-06-17T13:00:00+00:00",
                "timeClose": "2000-01-01T15:30:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-06-17T09:00:00+00:00",
                "timeLunch": "2023-06-17T12:00:00+00:00",
                "timeResume": "2023-06-17T13:00:00+00:00",
                "timeClose": "2000-01-01T15:30:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-06-17T09:00:00+00:00",
                "timeLunch": "2023-06-17T12:00:00+00:00",
                "timeResume": "2023-06-17T13:00:00+00:00",
                "timeClose": "2000-01-01T15:30:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-06-17T09:00:00+00:00",
                "timeLunch": "2023-06-17T12:00:00+00:00",
                "timeResume": "2023-06-17T13:00:00+00:00",
                "timeClose": "2000-01-01T15:30:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-06-17T09:00:00+00:00",
                "timeLunch": "2023-06-17T12:00:00+00:00",
                "timeResume": "2023-06-17T13:00:00+00:00",
                "timeClose": "2000-01-01T15:30:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "f9847b75-35f3-ed11-907c-6045bdd58fa1",
        "name": "Pure Screening Solutions, LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Gainesville, FL",
        "description": "The suburban professional plaza inside Jay-Jill Cosmetics Glamtique & Spa",
        "metaDescription": "Choose PrintScan in Gainesville, Florida for superior Live Scan and Fingerprinting services. We are committed to providing accurate and efficient identification solutions for your needs.",
        "notes": "Choose PrintScan in Gainesville, Florida for superior Live Scan and Fingerprinting services. We are committed to providing accurate and efficient identification solutions for your needs.",
        "address1": "4509 NW 23rd Ave",
        "address2": "STE 18",
        "stateCountry": "FL",
        "city": "Gainesville",
        "postalCode": "32606",
        "county": "Alachua",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -82.391465,
        "latitude": 29.673846,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T18:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T20:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T18:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T20:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T18:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T20:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T18:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T20:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T18:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T20:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "8563796e-36f3-ed11-907c-6045bdd58fa1",
        "name": "ARCpoint Labs of Roseville-Rocklin",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Rocklin, CA",
        "description": None,
        "metaDescription": "Visit PrintScan in Rocklin, California for premium Live Scan and Fingerprinting services. Our expert team provides precise and fast identification procedures. Trust in PrintScan Rocklin, CA for all your identification requirements with confidence.",
        "notes": "Visit PrintScan in Rocklin, California for premium Live Scan and Fingerprinting services. Our expert team provides precise and fast identification procedures. Trust in PrintScan Rocklin, CA for all your identification requirements with confidence.",
        "address1": "6681 Blue Oaks BLVD",
        "address2": "ste 1",
        "stateCountry": "CA",
        "city": "Rocklin",
        "postalCode": "95765",
        "county": "Placer",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -121.289347,
        "latitude": 38.796059,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:00:00-07:00",
                "timeLunch": "2000-01-01T11:30:00-07:00",
                "timeResume": "2023-05-15T13:00:00+00:00",
                "timeClose": "2000-01-01T16:00:00-07:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:00:00-07:00",
                "timeLunch": "2000-01-01T11:30:00-07:00",
                "timeResume": "2023-05-15T13:00:00+00:00",
                "timeClose": "2000-01-01T16:00:00-07:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:00:00-07:00",
                "timeLunch": "2000-01-01T11:30:00-07:00",
                "timeResume": "2023-05-15T13:00:00+00:00",
                "timeClose": "2000-01-01T16:00:00-07:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:00:00-07:00",
                "timeLunch": "2000-01-01T11:30:00-07:00",
                "timeResume": "2023-05-15T13:00:00+00:00",
                "timeClose": "2000-01-01T16:00:00-07:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:00:00-07:00",
                "timeLunch": "2000-01-01T11:30:00-07:00",
                "timeResume": "2023-05-15T13:00:00+00:00",
                "timeClose": "2000-01-01T16:00:00-07:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "9421c8c6-e7f3-ed11-907c-6045bdd58fa1",
        "name": "ARCpoint Labs of Libertyville",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Libertyville, IL",
        "description": "Just South of Peterson Rd and East of Hwy 45",
        "metaDescription": "Experience unparalleled Live Scan and Fingerprinting services at PrintScan in Libertyville, Illinois. Our dedicated professionals ensure accurate and efficient identification solutions. Choose PrintScan Libertyville, IL for trusted and reliable results.",
        "notes": "Experience unparalleled Live Scan and Fingerprinting services at PrintScan in Libertyville, Illinois. Our dedicated professionals ensure accurate and efficient identification solutions. Choose PrintScan Libertyville, IL for trusted and reliable results.",
        "address1": "1860 W Winchester Road",
        "address2": "Suite 205",
        "stateCountry": "IL",
        "city": "Libertyville",
        "postalCode": "60048",
        "county": "Lake",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -87.995252,
        "latitude": 42.296944,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-05-16T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-16T15:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-05-16T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-16T15:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-05-16T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-16T15:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-05-16T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-16T15:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-05-16T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-16T15:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "e28365f7-89f5-ed11-907c-6045bdd58fa1",
        "name": "ARCpoint Labs of Omaha",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Omaha, NE",
        "description": None,
        "metaDescription": "Turn to PrintScan in Omaha, Nebraska, your trusted destination for Live Scan and Fingerprinting services. Benefit from our speedy, secure, and confidential processes today.",
        "notes": "Turn to PrintScan in Omaha, Nebraska, your trusted destination for Live Scan and Fingerprinting services. Benefit from our speedy, secure, and confidential processes today.",
        "address1": "310 Regency Pkwy",
        "address2": "Suite 110",
        "stateCountry": "NE",
        "city": "Omaha",
        "postalCode": "68114",
        "county": "Douglas",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -96.074290,
        "latitude": 41.256789,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-05-18T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-18T16:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-05-18T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-18T16:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-05-18T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-18T16:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-05-18T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-18T16:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-05-18T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-18T16:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "a6c5cf07-8bf5-ed11-907c-6045bdd58fa1",
        "name": "ARCpoint Labs of Bakersfield",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Bakersfield, CA",
        "description": "Northwest Town Center",
        "metaDescription": "Discover top-notch Live Scan and Fingerprinting services at PrintScan in Bakersfield, California. We prioritize accuracy and efficiency in meeting all your identification requirements.",
        "notes": "Discover top-notch Live Scan and Fingerprinting services at PrintScan in Bakersfield, California. We prioritize accuracy and efficiency in meeting all your identification requirements.",
        "address1": "7737 Meany Ave",
        "address2": "Suite B9",
        "stateCountry": "CA",
        "city": "Bakersfield",
        "postalCode": "93308-5267",
        "county": "Kern",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -119.088355,
        "latitude": 35.393573,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-06-26T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-26T15:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-06-26T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-26T15:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-06-26T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-26T15:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-06-26T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-26T15:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-06-26T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-26T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "c283fab4-6c01-ee11-907c-6045bdd58fa1",
        "name": "Shelton Professional Services - Iron Mt",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Iron Mountain, MI",
        "description": None,
        "metaDescription": "Choose PrintScan in Iron Mountain, Michigan for your Live Scan and Fingerprinting needs. Our commitment to accuracy and speed ensures your identification process is seamless and reliable.",
        "notes": "Choose PrintScan in Iron Mountain, Michigan for your Live Scan and Fingerprinting needs. Our commitment to accuracy and speed ensures your identification process is seamless and reliable.",
        "address1": "1311 S. Stephenson Ave",
        "address2": "Suite 3",
        "stateCountry": "MI",
        "city": "Iron Mountain",
        "postalCode": "49801",
        "county": "Dickinson",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -88.056392,
        "latitude": 45.810229,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "53d9fd60-f3d2-ed11-8e8d-6045bddbb98a",
        "name": "Pronto Test Labs LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Mcallen, TX",
        "description": None,
        "metaDescription": "Visit PrintScan in Mcallen, Texas for professional Live Scan and Fingerprinting services. We specialize in providing comprehensive identification solutions for your security requirements.",
        "notes": "Visit PrintScan in Mcallen, Texas for professional Live Scan and Fingerprinting services. We specialize in providing comprehensive identification solutions for your security requirements.",
        "address1": "2215 N 23rd St.",
        "address2": None,
        "stateCountry": "TX",
        "city": "Mcallen",
        "postalCode": "78501",
        "county": "Hidalgo",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -98.242309,
        "latitude": 26.226203,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T10:00:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-06:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:00:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-06:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:00:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-06:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:00:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-06:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-06:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T09:30:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T12:00:00-06:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "49851888-0dd3-ed11-8e8d-6045bddbb98a",
        "name": "Sign and Stamp LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Louisville, KY",
        "description": "Next door to Witty's Party Supplies",
        "metaDescription": "Discover PrintScan in Louisville, Kentucky, your trusted provider for comprehensive Live Scan and Fingerprinting services. Rely on our quick, accurate, and dependable solutions to meet all your identification and verification needs.",
        "notes": "Discover PrintScan in Louisville, Kentucky, your trusted provider for comprehensive Live Scan and Fingerprinting services. Rely on our quick, accurate, and dependable solutions to meet all your identification and verification needs.",
        "address1": "3418 Frankfort Ave.",
        "address2": "Suite 260",
        "stateCountry": "KY",
        "city": "Louisville",
        "postalCode": "40207",
        "county": "Jefferson",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -85.668504,
        "latitude": 38.253608,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-07-14T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-14T15:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-07-14T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-14T15:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-07-14T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-14T15:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-07-14T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-14T15:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-07-14T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-14T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "6dfaefcb-a6d4-ed11-8e8d-6045bddbb98a",
        "name": "ARCpoint Labs of Cuyahoga Falls",
        "displayName": "Printscan Authorized Fingerprint Service Center - Cuyahoga Falls, OH",
        "description": None,
        "metaDescription": "Rely on PrintScan in Cuyahoga Falls, Ohio for your Live Scan and Fingerprinting needs. Our dedicated team delivers precise and fast results for all your identification solutions.",
        "notes": "Rely on PrintScan in Cuyahoga Falls, Ohio for your Live Scan and Fingerprinting needs. Our dedicated team delivers precise and fast results for all your identification solutions.",
        "address1": "960 Graham Road",
        "address2": "Unit 4",
        "stateCountry": "OH",
        "city": "Cuyahoga Falls",
        "postalCode": "44221",
        "county": "Summit",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.478523,
        "latitude": 41.162868,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-05-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-23T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-05-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-23T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-05-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-23T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-05-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-23T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-05-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-23T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "69ddfcac-a6d7-ed11-8e8d-6045bddbb98a",
        "name": "Guided Life Education Center",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Riverview, FL",
        "description": None,
        "metaDescription": "Trust PrintScan in Riverview, Florida for your Live Scan and Fingerprinting requirements. Our commitment to accuracy and efficiency ensures a seamless identification process for all our clients.",
        "notes": "Trust PrintScan in Riverview, Florida for your Live Scan and Fingerprinting requirements. Our commitment to accuracy and efficiency ensures a seamless identification process for all our clients.",
        "address1": "6323 US 301",
        "address2": None,
        "stateCountry": "FL",
        "city": "Riverview",
        "postalCode": "33578",
        "county": "Hillsborough",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -82.334577,
        "latitude": 27.889580,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-02T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-02T14:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-02T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-02T16:45:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-02T09:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-02T14:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-02T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-02T16:45:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-02T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-02T17:15:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "3449f7fc-34d9-ed11-8e8d-6045bddbb98a",
        "name": "Shelton Professional Services - Dearborn",
        "displayName": "Printscan Authorized Fingerprint Service Center - Dearborn, MI",
        "description": None,
        "metaDescription": "Discover unparalleled Live Scan and Fingerprinting services in Dearborn, Michigan with PrintScan. Your safety and satisfaction are our top priorities. Trust us for all your identification requirements.",
        "notes": "Discover unparalleled Live Scan and Fingerprinting services in Dearborn, Michigan with PrintScan. Your safety and satisfaction are our top priorities. Trust us for all your identification requirements.",
        "address1": "22976 W Outer Dr",
        "address2": None,
        "stateCountry": "MI",
        "city": "Dearborn",
        "postalCode": "48124",
        "county": "Wayne",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -83.218163,
        "latitude": 42.277804,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-04-19T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-19T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-04-19T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-19T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "824041dc-54d9-ed11-8e8d-6045bddbb98a",
        "name": "Goin Postal Easton",
        "displayName": "Printscan Authorized Fingerprint Service Center - Easton, PA",
        "description": None,
        "metaDescription": "Choose PrintScan in Easton, Pennsylvania for superior Live Scan and Fingerprinting services. Our commitment to precision and speed ensures your identification needs are met effectively.",
        "notes": "Choose PrintScan in Easton, Pennsylvania for superior Live Scan and Fingerprinting services. Our commitment to precision and speed ensures your identification needs are met effectively.",
        "address1": "2430 Butler Street",
        "address2": None,
        "stateCountry": "PA",
        "city": "Easton",
        "postalCode": "18042",
        "county": "Northampton",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -75.246622,
        "latitude": 40.682225,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-05-04T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-04T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-05-04T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-04T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-05-04T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-04T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-05-04T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-04T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-05-04T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-04T16:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-05-04T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-04T12:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "3b1744ca-55d9-ed11-8e8d-6045bddbb98a",
        "name": "The Packaging Place",
        "displayName": "Printscan Authorized Fingerprint Service Center - East Stroudsburg, PA",
        "description": "Use 722 Milford Road for GPS to get to the front door.",
        "metaDescription": "Experience fast and reliable Live Scan and Fingerprinting services at PrintScan in East Stroudsburg, Pennsylvania. Trust our experts for secure, efficient, and high-quality fingerprinting solutions.",
        "notes": "Experience fast and reliable Live Scan and Fingerprinting services at PrintScan in East Stroudsburg, Pennsylvania. Trust our experts for secure, efficient, and high-quality fingerprinting solutions.",
        "address1": "730 Milford Road",
        "address2": "Suite 16",
        "stateCountry": "PA",
        "city": "East Stroudsburg",
        "postalCode": "18301",
        "county": "Monroe",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -75.180051,
        "latitude": 41.018675,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-29T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T18:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-29T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T18:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-29T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T18:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-29T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T18:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-29T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T18:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-07-31T08:45:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-31T13:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "8094b019-5ad9-ed11-8e8d-6045bddbb98a",
        "name": "CRC Onboarding Services - Raleigh, NC",
        "displayName": "Printscan Authorized Fingerprint Service Center - Raleigh NC",
        "description": None,
        "metaDescription": "Choose PrintScan in Raleigh, North Carolina for your Live Scan and Fingerprinting needs. Our expert team delivers high-quality, accurate, and speedy identification services.",
        "notes": "Choose PrintScan in Raleigh, North Carolina for your Live Scan and Fingerprinting needs. Our expert team delivers high-quality, accurate, and speedy identification services.",
        "address1": "4020 Wake Forest Road",
        "address2": "Ste 214",
        "stateCountry": "NC",
        "city": "Raleigh",
        "postalCode": "27609",
        "county": "Wake",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -78.614053,
        "latitude": 35.835442,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-06-07T09:00:00+00:00",
                "timeLunch": "2023-06-07T12:30:00+00:00",
                "timeResume": "2023-06-07T14:00:00+00:00",
                "timeClose": "2023-06-07T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-06-07T09:00:00+00:00",
                "timeLunch": "2023-06-07T12:30:00+00:00",
                "timeResume": "2023-06-07T14:00:00+00:00",
                "timeClose": "2023-06-07T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-06-07T09:00:00+00:00",
                "timeLunch": "2023-06-07T12:30:00+00:00",
                "timeResume": "2023-06-07T14:00:00+00:00",
                "timeClose": "2023-06-07T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-06-07T09:00:00+00:00",
                "timeLunch": "2023-06-07T12:30:00+00:00",
                "timeResume": "2023-06-07T14:00:00+00:00",
                "timeClose": "2023-06-07T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-06-07T09:00:00+00:00",
                "timeLunch": "2023-06-07T12:30:00+00:00",
                "timeResume": "2023-06-07T14:00:00+00:00",
                "timeClose": "2023-06-07T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "0861e390-76d9-ed11-8e8d-6045bddbb98a",
        "name": "CRC Onboarding Services - Durham, NC",
        "displayName": "Printscan Authorized Fingerprint Service Center - Durham, NC",
        "description": None,
        "metaDescription": "Choose PrintScan in Durham, North Carolina for exceptional Live Scan and Fingerprinting services. We provide accurate and swift results to meet your safety and security demands.",
        "notes": "Choose PrintScan in Durham, North Carolina for exceptional Live Scan and Fingerprinting services. We provide accurate and swift results to meet your safety and security demands.",
        "address1": "5107 Southpark Drive",
        "address2": "Suite 206",
        "stateCountry": "NC",
        "city": "Durham",
        "postalCode": "27713",
        "county": "Chatham",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -78.942932,
        "latitude": 35.911280,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-06-19T09:00:00+00:00",
                "timeLunch": "2023-06-19T12:00:00+00:00",
                "timeResume": "2023-06-19T13:30:00+00:00",
                "timeClose": "2023-06-19T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-06-19T09:00:00+00:00",
                "timeLunch": "2023-06-19T12:00:00+00:00",
                "timeResume": "2023-06-19T13:30:00+00:00",
                "timeClose": "2023-06-19T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-06-19T09:00:00+00:00",
                "timeLunch": "2023-06-19T12:00:00+00:00",
                "timeResume": "2023-06-19T13:30:00+00:00",
                "timeClose": "2023-06-19T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-06-19T09:00:00+00:00",
                "timeLunch": "2023-06-19T12:00:00+00:00",
                "timeResume": "2023-06-19T13:30:00+00:00",
                "timeClose": "2023-06-19T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-06-19T09:00:00+00:00",
                "timeLunch": "2023-06-19T12:00:00+00:00",
                "timeResume": "2023-06-19T13:30:00+00:00",
                "timeClose": "2023-06-19T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "96c8401f-27da-ed11-8e8d-6045bddbb98a",
        "name": "White Sands Drug and Alcohol Compliance",
        "displayName": "Printscan Authorized Fingerprint Service Center - Alamogordo, NM",
        "description": "Directly behind the rec center",
        "metaDescription": "Discover top-notch Live Scan and Fingerprinting services at PrintScan in Alamogordo, New Mexico. Your go-to destination for secure, accurate, and professional fingerprinting needs.",
        "notes": "Discover top-notch Live Scan and Fingerprinting services at PrintScan in Alamogordo, New Mexico. Your go-to destination for secure, accurate, and professional fingerprinting needs.",
        "address1": "1110 WASHINGTON AVE",
        "address2": None,
        "stateCountry": "NM",
        "city": "Alamogordo",
        "postalCode": "88310",
        "county": "Otero",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -105.943230,
        "latitude": 32.901567,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-04-13T07:00:00+00:00",
                "timeLunch": "2023-04-13T12:00:00+00:00",
                "timeResume": "2023-04-13T13:00:00+00:00",
                "timeClose": "2023-04-13T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-04-13T07:00:00+00:00",
                "timeLunch": "2023-04-13T12:00:00+00:00",
                "timeResume": "2023-04-13T13:00:00+00:00",
                "timeClose": "2023-04-13T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-04-13T07:00:00+00:00",
                "timeLunch": "2023-04-13T12:00:00+00:00",
                "timeResume": "2023-04-13T13:00:00+00:00",
                "timeClose": "2023-04-13T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-04-13T07:00:00+00:00",
                "timeLunch": "2023-04-13T12:00:00+00:00",
                "timeResume": "2023-04-13T13:00:00+00:00",
                "timeClose": "2023-04-13T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-04-13T07:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-13T11:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "ccfda420-30da-ed11-8e8d-6045bddbb98a",
        "name": "AZC Drug Testing",
        "displayName": "Printscan Authorized Fingerprint Service Center - Sierra Vista , AZ",
        "description": "NW corner of Hwy 92 & Foothills Dr.",
        "metaDescription": "Choose PrintScan in Sierra Vista, Arizona for superior Live Scan and Fingerprinting services. We prioritize your security with our precise and efficient fingerprinting solutions.",
        "notes": "Choose PrintScan in Sierra Vista, Arizona for superior Live Scan and Fingerprinting services. We prioritize your security with our precise and efficient fingerprinting solutions.",
        "address1": "3965 E Foothills Dr.",
        "address2": "Suite I",
        "stateCountry": "AZ",
        "city": "Sierra Vista",
        "postalCode": "85635",
        "county": "Cochise",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -110.258196,
        "latitude": 31.545737,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-04-13T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-13T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-04-13T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-13T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-04-13T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-13T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-04-13T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-13T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-04-13T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-13T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "f0c73a26-42dd-ed11-8e8d-6045bddbb98a",
        "name": "A1 Postal Services",
        "displayName": "Printscan Authorized Fingerprint Service Center - Port St Lucie, FL",
        "description": None,
        "metaDescription": "Discover unparalleled Live Scan and Fingerprinting services at PrintScan in Port Saint Lucie, Florida. Our experienced team delivers fast, precise, and reliable solutions for all your identification needs. Rely on PrintScan Port Saint Lucie for secure and efficient services.",
        "notes": "Discover unparalleled Live Scan and Fingerprinting services at PrintScan in Port Saint Lucie, Florida. Our experienced team delivers fast, precise, and reliable solutions for all your identification needs. Rely on PrintScan Port Saint Lucie for secure and efficient services.",
        "address1": "11582 SW Village Parkway",
        "address2": None,
        "stateCountry": "FL",
        "city": "Port St Lucie",
        "postalCode": "34987",
        "county": "Saint Lucie",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.427829,
        "latitude": 27.256860,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-07-28T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-28T18:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-07-28T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-28T18:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-07-28T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-28T18:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-07-28T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-28T18:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-07-28T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-28T18:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-07-28T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-28T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "1b029925-0bde-ed11-8e8d-6045bddbb98a",
        "name": "Southern Background Services LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Hazlehurst, GA",
        "description": None,
        "metaDescription": "Choose PrintScan in Hazlehurst, Georgia for unparalleled Live Scan and Fingerprinting services. We provide secure, precise, and swift fingerprinting solutions to cater to your individual needs.",
        "notes": "Choose PrintScan in Hazlehurst, Georgia for unparalleled Live Scan and Fingerprinting services. We provide secure, precise, and swift fingerprinting solutions to cater to your individual needs.",
        "address1": "9 Latimer St.",
        "address2": None,
        "stateCountry": "GA",
        "city": "Hazlehurst",
        "postalCode": "31539",
        "county": "Jeff Davis",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -82.598961,
        "latitude": 31.866217,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:45:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:45:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:45:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:45:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:45:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "8bb1143d-0ede-ed11-8e8d-6045bddbb98a",
        "name": "Postal Shoppe",
        "displayName": "Printscan Authorized Fingerprint Service Center - Rockford, IL",
        "description": None,
        "metaDescription": "Trust PrintScan in Rockford, Illinois for top-tier Live Scan and Fingerprinting services. We are dedicated to delivering secure, accurate, and prompt fingerprinting solutions for all your needs.",
        "notes": "Trust PrintScan in Rockford, Illinois for top-tier Live Scan and Fingerprinting services. We are dedicated to delivering secure, accurate, and prompt fingerprinting solutions for all your needs.",
        "address1": "1643 N Alpine Road",
        "address2": "Suite 104",
        "stateCountry": "IL",
        "city": "Rockford",
        "postalCode": "61107",
        "county": "Winnebago",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -89.026328,
        "latitude": 42.286438,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "126e3aab-c1de-ed11-8e8d-6045bddbb98a",
        "name": "White Glove Drug & Alcohol Testing",
        "displayName": "Printscan Authorized Fingerprint Service Center - Severna Park, MD",
        "description": "Same Building as Jimmy Johns",
        "metaDescription": "Experience exceptional Live Scan and Fingerprinting services at PrintScan in Severna Park, Maryland. We are committed to providing secure, precise, and efficient fingerprinting solutions to meet your specific requirements.",
        "notes": "Experience exceptional Live Scan and Fingerprinting services at PrintScan in Severna Park, Maryland. We are committed to providing secure, precise, and efficient fingerprinting solutions to meet your specific requirements.",
        "address1": "537 Ritchie Highway",
        "address2": "Suite 2E",
        "stateCountry": "MD",
        "city": "Severna Park",
        "postalCode": "21146",
        "county": "Anne Arundel",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -76.546068,
        "latitude": 39.078736,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-08T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-08T16:45:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-08T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-08T16:45:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-08T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-08T16:45:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-08T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-08T16:45:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-08T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-08T16:45:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "84630c62-c8de-ed11-8e8d-6045bddbb98a",
        "name": "ACTDT",
        "displayName": "Printscan Authorized Fingerprint Service Center - El Paso, TX",
        "description": None,
        "metaDescription": "Experience fast and reliable Live Scan and Fingerprinting services in El Paso, Texas with PrintScan. We're committed to providing top-notch security solutions for your identification needs.",
        "notes": "Experience fast and reliable Live Scan and Fingerprinting services in El Paso, Texas with PrintScan. We're committed to providing top-notch security solutions for your identification needs.",
        "address1": "7501 Lockheed Dr",
        "address2": "STE D",
        "stateCountry": "TX",
        "city": "El Paso",
        "postalCode": "79925",
        "county": "El Paso",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -106.388105,
        "latitude": 31.791290,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-04-19T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-19T16:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-04-19T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-19T16:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-04-19T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-19T16:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "60fbfab4-84df-ed11-8e8d-6045bddbb98a",
        "name": "Lifeline Enterprises LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Orchard Beach, MD",
        "description": None,
        "metaDescription": "Choose PrintScan in Halethorpe, Maryland for top-notch Live Scan and Fingerprinting services. We prioritize your security with our precise, efficient, and high-quality fingerprinting solutions.",
        "notes": "Choose PrintScan in Halethorpe, Maryland for top-notch Live Scan and Fingerprinting services. We prioritize your security with our precise, efficient, and high-quality fingerprinting solutions.",
        "address1": "611 Hilltop Rd",
        "address2": None,
        "stateCountry": "MD",
        "city": "Orchard Beach",
        "postalCode": "21226",
        "county": "Anne Arundel",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -76.530545,
        "latitude": 39.168394,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 0,
                "timeOpen": "2023-05-12T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-12T15:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-05-12T14:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-12T17:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-05-12T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-12T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "2ccbd600-52e0-ed11-8e8d-6045bddbb98a",
        "name": "Alpha Screening Services",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Westland, MI",
        "description": None,
        "metaDescription": "Visit PrintScan in Westland, Michigan for premium Live Scan and Fingerprinting services. We offer secure, fast, and reliable fingerprinting solutions tailored to your specific needs.",
        "notes": "Visit PrintScan in Westland, Michigan for premium Live Scan and Fingerprinting services. We offer secure, fast, and reliable fingerprinting solutions tailored to your specific needs.",
        "address1": "35360 Nankin BLVD",
        "address2": "STE 801",
        "stateCountry": "MI",
        "city": "Westland",
        "postalCode": "48185",
        "county": "Wayne",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -83.389747,
        "latitude": 42.345892,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T12:15:00-05:00",
                "timeLunch": "2023-04-21T13:00:00+00:00",
                "timeResume": "2023-04-21T14:00:00+00:00",
                "timeClose": "2000-01-01T15:45:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T12:15:00-05:00",
                "timeLunch": "2023-04-21T13:00:00+00:00",
                "timeResume": "2023-04-21T14:00:00+00:00",
                "timeClose": "2000-01-01T15:45:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T12:15:00-05:00",
                "timeLunch": "2023-04-21T13:00:00+00:00",
                "timeResume": "2023-04-21T14:00:00+00:00",
                "timeClose": "2000-01-01T15:45:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T12:15:00-05:00",
                "timeLunch": "2023-04-21T13:00:00+00:00",
                "timeResume": "2023-04-21T14:00:00+00:00",
                "timeClose": "2000-01-01T15:45:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b4d6a14f-a2e2-ed11-8e8d-6045bddbb98a",
        "name": "Postal Pros Plus LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Lantana, FL",
        "description": None,
        "metaDescription": "Choose PrintScan in Lantana, Florida, your reliable source for top-notch Live Scan and Fingerprinting services. Benefit from our swift, secure, and bespoke solutions tailored to meet your unique requirements.",
        "notes": "Choose PrintScan in Lantana, Florida, your reliable source for top-notch Live Scan and Fingerprinting services. Benefit from our swift, secure, and bespoke solutions tailored to meet your unique requirements.",
        "address1": "928 South Dixie Highway",
        "address2": None,
        "stateCountry": "FL",
        "city": "Lantana",
        "postalCode": "33462",
        "county": "Palm Beach",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.053023,
        "latitude": 26.576885,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T11:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T11:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T11:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T11:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T11:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "63165581-a3e2-ed11-8e8d-6045bddbb98a",
        "name": "Charmante Laboratory LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Daytona Beach, FL",
        "description": None,
        "metaDescription": "Discover top-notch Live Scan and Fingerprinting solutions at PrintScan in Daytona Beach, Florida. We're committed to providing accurate and efficient identification services for your peace of mind.",
        "notes": "Discover top-notch Live Scan and Fingerprinting solutions at PrintScan in Daytona Beach, Florida. We're committed to providing accurate and efficient identification services for your peace of mind.",
        "address1": "140 South Beach Street",
        "address2": "#303",
        "stateCountry": "FL",
        "city": "Daytona Beach",
        "postalCode": "32114",
        "county": "Volusia",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.019194,
        "latitude": 29.211054,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-07-18T14:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-18T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "53b6aa80-a4e2-ed11-8e8d-6045bddbb98a",
        "name": "Front Line Industries LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - White Bear Lake, MN",
        "description": None,
        "metaDescription": "Choose PrintScan in White Bear Lake, Minnesota for superior Live Scan and Fingerprinting services. We offer efficient, secure, and reliable solutions for all your identification needs.",
        "notes": "Choose PrintScan in White Bear Lake, Minnesota for superior Live Scan and Fingerprinting services. We offer efficient, secure, and reliable solutions for all your identification needs.",
        "address1": "1310 Highway 96 E",
        "address2": "Suite 235",
        "stateCountry": "MN",
        "city": "White Bear Lake",
        "postalCode": "55110",
        "county": "Ramsey",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -93.046023,
        "latitude": 45.078680,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-05-30T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-30T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-05-30T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-30T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-05-30T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-30T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-06-15T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-15T12:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "c00d47ce-f8e4-ed11-8e8d-6045bddbb98a",
        "name": "Grand Lakes Postal",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Katy, TX",
        "description": None,
        "metaDescription": "Choose PrintScan in Katy, Texas, your trusted provider for Live Scan and Fingerprinting services. We offer quick, secure, and tailored identification solutions to match your individual needs.",
        "notes": "Choose PrintScan in Katy, Texas, your trusted provider for Live Scan and Fingerprinting services. We offer quick, secure, and tailored identification solutions to match your individual needs.",
        "address1": "5554 S Peek Road",
        "address2": None,
        "stateCountry": "TX",
        "city": "Katy",
        "postalCode": "77450",
        "county": "Waller",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -95.765414,
        "latitude": 29.714242,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-06-14T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-14T17:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-06-14T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-14T17:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-06-14T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-14T17:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-06-14T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-14T17:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-06-14T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-14T17:30:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-06-14T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-14T13:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b9b3dcd9-c8e5-ed11-8e8d-6045bddbb98a",
        "name": "Shelton Professional Services - Marquette",
        "displayName": "Printscan Authorized Fingerprint Service Center - Marquette, MI",
        "description": None,
        "metaDescription": "Get reliable and quick Live Scan and Fingerprinting services at PrintScan in Marquette, Michigan. Our dedicated professionals are here to cater to all your identification needs. Visit us for a seamless experience today!",
        "notes": "Get reliable and quick Live Scan and Fingerprinting services at PrintScan in Marquette, Michigan. Our dedicated professionals are here to cater to all your identification needs. Visit us for a seamless experience today!",
        "address1": "201 Rublein St",
        "address2": "Suite C",
        "stateCountry": "MI",
        "city": "Marquette",
        "postalCode": "49855",
        "county": "Marquette",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -87.418545,
        "latitude": 46.547128,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-07-12T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-12T16:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-07-12T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-12T16:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-07-12T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-12T16:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-07-12T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-12T16:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-07-12T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-12T16:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "be857f6f-fbe5-ed11-8e8d-6045bddbb98a",
        "name": "Greenaway's Lab Essential Testing & Screening LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Houston, TX",
        "description": None,
        "metaDescription": "Discover PrintScan in Houston, Texas, your premier choice for top-notch Live Scan and Fingerprinting services. Enjoy our speedy, secure, and trusted fingerprinting solutions at PrintScan Houston today.",
        "notes": "Discover PrintScan in Houston, Texas, your premier choice for top-notch Live Scan and Fingerprinting services. Enjoy our speedy, secure, and trusted fingerprinting solutions at PrintScan Houston today.",
        "address1": "13700 Veterans Memorial",
        "address2": "Suite 240B",
        "stateCountry": "TX",
        "city": "Houston",
        "postalCode": "77014",
        "county": "Harris",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -95.495397,
        "latitude": 29.984900,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-09-22T09:00:00+00:00",
                "timeLunch": "2023-09-22T12:30:00+00:00",
                "timeResume": "2023-09-22T13:00:00+00:00",
                "timeClose": "2023-09-22T16:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-09-22T09:00:00+00:00",
                "timeLunch": "2023-09-22T12:30:00+00:00",
                "timeResume": "2023-09-22T13:00:00+00:00",
                "timeClose": "2023-09-22T16:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-09-22T09:00:00+00:00",
                "timeLunch": "2023-09-22T12:30:00+00:00",
                "timeResume": "2023-09-22T13:00:00+00:00",
                "timeClose": "2023-09-22T16:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-09-22T09:00:00+00:00",
                "timeLunch": "2023-09-22T12:30:00+00:00",
                "timeResume": "2023-09-22T13:00:00+00:00",
                "timeClose": "2023-09-22T16:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-09-22T09:00:00+00:00",
                "timeLunch": "2023-09-22T12:30:00+00:00",
                "timeResume": "2023-09-22T13:00:00+00:00",
                "timeClose": "2023-09-22T16:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "f6cde167-e4e9-ed11-8e8d-6045bddbb98a",
        "name": "ARCpoint Labs of Washington DC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Washington, DC",
        "description": "On the corner of Yuma St NW and Massachustetts Ave NW",
        "metaDescription": "Experience fast and accurate Live Scan and Fingerprinting services at PrintScan in Washington, DC. Our dedicated team ensures a seamless process for all your identification needs.",
        "notes": "Experience fast and accurate Live Scan and Fingerprinting services at PrintScan in Washington, DC. Our dedicated team ensures a seamless process for all your identification needs.",
        "address1": "4910 Massachusetts Ave, NW",
        "address2": "Ste 219",
        "stateCountry": "DC",
        "city": "Washington",
        "postalCode": "20016",
        "county": "District Of Columbia",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -77.098084,
        "latitude": 38.946061,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-05-03T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-03T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-05-03T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-03T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-05-03T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-03T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-05-03T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-03T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-05-03T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-03T17:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-05-03T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-03T13:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "18842b44-e9e9-ed11-8e8d-6045bddbb98a",
        "name": "DNA Drug and Alcohol Centers",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Howell, MI",
        "description": None,
        "metaDescription": "Visit PrintScan in Howell, Michigan for your Live Scan and Fingerprinting requirements. Our team is dedicated to providing fast and accurate identification services. Experience our exceptional customer service today!",
        "notes": "Visit PrintScan in Howell, Michigan for your Live Scan and Fingerprinting requirements. Our team is dedicated to providing fast and accurate identification services. Experience our exceptional customer service today!",
        "address1": "736 South Michigan Ave",
        "address2": None,
        "stateCountry": "MI",
        "city": "Howell",
        "postalCode": "48843",
        "county": "Livingston",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -83.933956,
        "latitude": 42.601181,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 0,
                "timeOpen": "2023-05-03T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T09:45:00-05:00"
            },
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-05-03T07:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-05-03T07:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-05-03T07:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-05-03T07:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-05-03T07:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-05-03T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T09:45:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "062df416-ebe9-ed11-8e8d-6045bddbb98a",
        "name": "Integrity Drug Screening",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Livingston, TX",
        "description": "On the corner of W Polk St and N Oak Ave",
        "metaDescription": "Choose PrintScan in Livingston, Texas for all your Live Scan and Fingerprinting needs. Our team is committed to delivering fast, accurate, and reliable identification services. Visit us today for an unparalleled experience!",
        "notes": "Choose PrintScan in Livingston, Texas for all your Live Scan and Fingerprinting needs. Our team is committed to delivering fast, accurate, and reliable identification services. Visit us today for an unparalleled experience!",
        "address1": "624 W Polk St",
        "address2": None,
        "stateCountry": "TX",
        "city": "Livingston",
        "postalCode": "77351",
        "county": "Polk",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -94.938521,
        "latitude": 30.711933,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-05-03T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-03T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-05-03T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-03T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-05-03T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-03T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-05-03T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-03T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-05-03T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-03T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "bf7c0291-ece9-ed11-8e8d-6045bddbb98a",
        "name": "Absolute Solutions",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Lagrange, GA",
        "description": "On Mooty Brdge Road betoween Private St and Malibu Drive",
        "metaDescription": "Rely on PrintScan in Lagrange, Georgia for high-quality Live Scan and Fingerprinting services. We prioritize speed and accuracy in all our identification solutions. Experience our superior service today!",
        "notes": "Rely on PrintScan in Lagrange, Georgia for high-quality Live Scan and Fingerprinting services. We prioritize speed and accuracy in all our identification solutions. Experience our superior service today!",
        "address1": "1113 Mooty Bridge Rd",
        "address2": None,
        "stateCountry": "GA",
        "city": "Lagrange",
        "postalCode": "30240",
        "county": "Troup",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -85.035413,
        "latitude": 33.060110,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-11T09:00:00+00:00",
                "timeLunch": "2023-08-11T11:00:00+00:00",
                "timeResume": "2023-08-11T13:00:00+00:00",
                "timeClose": "2023-08-11T15:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-11T09:00:00+00:00",
                "timeLunch": "2023-08-11T11:00:00+00:00",
                "timeResume": "2023-08-11T13:00:00+00:00",
                "timeClose": "2023-08-11T15:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-11T09:00:00+00:00",
                "timeLunch": "2023-08-11T11:00:00+00:00",
                "timeResume": "2023-08-11T13:00:00+00:00",
                "timeClose": "2023-08-11T15:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-11T09:00:00+00:00",
                "timeLunch": "2023-08-11T11:00:00+00:00",
                "timeResume": "2023-08-11T13:00:00+00:00",
                "timeClose": "2023-08-11T15:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-11T09:00:00+00:00",
                "timeLunch": "2023-08-11T11:00:00+00:00",
                "timeResume": "2023-08-11T13:00:00+00:00",
                "timeClose": "2023-08-11T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "9394162e-ede9-ed11-8e8d-6045bddbb98a",
        "name": "e-Lab Quick LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Peoria, GA",
        "description": "Tanglewood Shopping Plaza",
        "metaDescription": "Visit PrintScan in Peoria, Illinois for fast and precise Live Scan and Fingerprinting services. Our dedicated team is here to meet all your identification needs with professionalism and accuracy. Stop by today!",
        "notes": "Visit PrintScan in Peoria, Illinois for fast and precise Live Scan and Fingerprinting services. Our dedicated team is here to meet all your identification needs with professionalism and accuracy. Stop by today!",
        "address1": "6926 N University St",
        "address2": "Ste F",
        "stateCountry": "IL",
        "city": "Peoria",
        "postalCode": "61614",
        "county": "Peoria",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -89.616172,
        "latitude": 40.772946,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-05-03T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-03T15:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-05-03T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-03T15:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-01T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-01T15:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-05-03T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-03T15:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-05-03T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-03T15:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b78beb2b-b2ea-ed11-8e8d-6045bddbb98a",
        "name": "ARCpoint Labs of The Woodlands TX",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Woodlands, TX",
        "description": "west side of the retail center-cross street is Research Park Drive",
        "metaDescription": "Experience top-tier Live Scan and Fingerprinting services at PrintScan in Woodlands, Texas. Our team is committed to providing swift, accurate identification solutions. Visit us today for your needs!",
        "notes": "Experience top-tier Live Scan and Fingerprinting services at PrintScan in Woodlands, Texas. Our team is committed to providing swift, accurate identification solutions. Visit us today for your needs!",
        "address1": "2520 Research Forest Drive",
        "address2": "Ste 400",
        "stateCountry": "TX",
        "city": "The Woodlands",
        "postalCode": "77381",
        "county": "Montgomery",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -95.475769,
        "latitude": 30.177430,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-06:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-06:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-06:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-06:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-06:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "8d4b07d5-d0ed-ed11-8e8d-6045bddbb98a",
        "name": "TodoModo LLC DBA: Fastest Labs of Sarasota",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Sarasota, FL",
        "description": None,
        "metaDescription": "Discover PrintScan in Sarasota, Florida, your trusted hub for exceptional Live Scan and Fingerprinting services. Experience our quick, secure, and personalized solutions designed to suit your individual needs.",
        "notes": "Discover PrintScan in Sarasota, Florida, your trusted hub for exceptional Live Scan and Fingerprinting services. Experience our quick, secure, and personalized solutions designed to suit your individual needs.",
        "address1": "2650 Bahia Vista Street",
        "address2": "Suite 302",
        "stateCountry": "FL",
        "city": "Sarasota",
        "postalCode": "34239",
        "county": "Sarasota",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -82.516827,
        "latitude": 27.322439,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "209c2633-35f0-ed11-8e8d-6045bddbb98a",
        "name": "Great Expectations of Lake County",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Leesburg, FL",
        "description": None,
        "metaDescription": "Choose PrintScan in Leesburg, Florida for top-tier Live Scan and Fingerprinting services. Our expert team provides accurate and swift results, catering to all your identification needs with utmost professionalism.",
        "notes": "Choose PrintScan in Leesburg, Florida for top-tier Live Scan and Fingerprinting services. Our expert team provides accurate and swift results, catering to all your identification needs with utmost professionalism.",
        "address1": "1310 West North Blvd.",
        "address2": "Suite 2",
        "stateCountry": "FL",
        "city": "Leesburg",
        "postalCode": "34748",
        "county": "Lake",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.883906,
        "latitude": 28.823533,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-06-26T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-26T15:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-06-26T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-26T15:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-06-26T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-26T15:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-06-26T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-26T15:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-06-26T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-26T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "9b9bc7ad-39f0-ed11-8e8d-6045bddbb98a",
        "name": "GodDSource LLC DBA: High Tech Express",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Austell, Georgia",
        "description": None,
        "metaDescription": "Choose PrintScan in Austell, Georgia for reliable and efficient Live Scan and Fingerprinting services. Our team is dedicated to providing accurate identification solutions swiftly. Experience our exceptional service today!",
        "notes": "Choose PrintScan in Austell, Georgia for reliable and efficient Live Scan and Fingerprinting services. Our team is dedicated to providing accurate identification solutions swiftly. Experience our exceptional service today!",
        "address1": "4427 Austell Road",
        "address2": "Suite 126",
        "stateCountry": "GA",
        "city": "Austell",
        "postalCode": "30106",
        "county": "Cobb",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -84.608867,
        "latitude": 33.845777,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-21T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "5a03e96e-3af0-ed11-8e8d-6045bddbb98a",
        "name": "Stat Diagnostics LLC - Woodbridge",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Woodbridge, Virginia",
        "description": None,
        "metaDescription": "Visit PrintScan in Woodbridge, Virginia for exceptional Live Scan and Fingerprinting services. Our dedicated team provides rapid and precise results for all your identification needs. Trust PrintScan Woodbridge for secure, efficient, and professional fingerprinting solutions.",
        "notes": "Visit PrintScan in Woodbridge, Virginia for exceptional Live Scan and Fingerprinting services. Our dedicated team provides rapid and precise results for all your identification needs. Trust PrintScan Woodbridge for secure, efficient, and professional fingerprinting solutions.",
        "address1": "4308 Ridgewood Center Drive",
        "address2": None,
        "stateCountry": "VA",
        "city": "Woodbridge",
        "postalCode": "22192",
        "county": "Prince William",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -77.338987,
        "latitude": 38.673541,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T14:00:00-05:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T14:00:00-05:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T14:00:00-05:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T14:00:00-05:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T14:00:00-05:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "f6baf68a-64b4-ed11-a8de-6045bdee2d76",
        "name": "Nashville Process Services",
        "displayName": "PrintScan - Authorized Fingerprint Service Center",
        "description": "Please contact 615-571-3711 when you are in the lobby, and we will bring you up (or at entrance on Saturdays)",
        "metaDescription": "Choose PrintScan in Nashville, Tennessee for premier Live Scan and Fingerprinting services. We provide high-quality, reliable identification solutions tailored to your specific needs.",
        "notes": "Choose PrintScan in Nashville, Tennessee for premier Live Scan and Fingerprinting services. We provide high-quality, reliable identification solutions tailored to your specific needs.",
        "address1": "555 Mariott Dr",
        "address2": "Suite 315",
        "stateCountry": "TN",
        "city": "Nashville",
        "postalCode": "37214",
        "county": "Davidson",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -86.689513,
        "latitude": 36.148055,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-04-24T08:00:00+00:00",
                "timeLunch": "2023-04-24T11:30:00+00:00",
                "timeResume": "2023-04-24T12:30:00+00:00",
                "timeClose": "2023-04-24T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-04-24T08:00:00+00:00",
                "timeLunch": "2023-04-24T11:30:00+00:00",
                "timeResume": "2023-04-24T12:30:00+00:00",
                "timeClose": "2023-04-24T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-04-24T08:00:00+00:00",
                "timeLunch": "2023-04-24T11:30:00+00:00",
                "timeResume": "2023-04-24T12:30:00+00:00",
                "timeClose": "2023-04-24T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-04-24T08:00:00+00:00",
                "timeLunch": "2023-04-24T11:30:00+00:00",
                "timeResume": "2023-04-24T12:30:00+00:00",
                "timeClose": "2023-04-24T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-04-24T08:00:00+00:00",
                "timeLunch": "2023-04-24T11:30:00+00:00",
                "timeResume": "2023-04-24T12:30:00+00:00",
                "timeClose": "2023-04-24T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "570e7bb7-13b9-ed11-a8de-6045bdee2d76",
        "name": "Deez Global Enterprise",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Long Beach, CA",
        "description": "Turn right when you exit the elevator.",
        "metaDescription": "Visit PrintScan in Long Beach, California, your trusted source for superior Live Scan and Fingerprinting services. Count on PrintScan Long Beach, CA for dependable, quick, and accurate fingerprinting needs.",
        "notes": "Visit PrintScan in Long Beach, California, your trusted source for superior Live Scan and Fingerprinting services. Count on PrintScan Long Beach, CA for dependable, quick, and accurate fingerprinting needs.",
        "address1": "3711 Long Beach Boulevard",
        "address2": "4th Floor, Room 4057",
        "stateCountry": "CA",
        "city": "Long Beach",
        "postalCode": "90807",
        "county": "Los Angeles",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -118.189586,
        "latitude": 33.824277,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T14:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T19:00:00-07:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-07-27T16:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T19:00:00-07:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "a6cb7d55-67bc-ed11-a8de-6045bdee2d76",
        "name": "Endless DOT Services LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Laredo, TX",
        "description": None,
        "metaDescription": "Explore superior Live Scan and Fingerprinting services at PrintScan in Laredo, Texas. Our advanced technology guarantees swift and accurate results for all your personal and professional identification needs.",
        "notes": "Explore superior Live Scan and Fingerprinting services at PrintScan in Laredo, Texas. Our advanced technology guarantees swift and accurate results for all your personal and professional identification needs.",
        "address1": "5701 Springfield Avenue",
        "address2": None,
        "stateCountry": "TX",
        "city": "Laredo",
        "postalCode": "78041",
        "county": "Webb",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -99.490648,
        "latitude": 27.547169,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-03-06T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-06T18:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-03-06T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-06T18:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-03-06T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-06T18:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-03-06T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-06:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-03-06T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-06:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-03-06T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-06T14:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "eded93b3-0bbd-ed11-a8de-6045bdee2d76",
        "name": "100 Percent Verified Staging Test",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Corona, CA",
        "description": "OFFICE IS LOCATED IN SUITE 105",
        "metaDescription": "Rely on PrintScan in Corona, California for state-of-the-art Live Scan and Fingerprinting services. Our expert team delivers precise and swift identity verification to meet your unique needs.",
        "notes": "Rely on PrintScan in Corona, California for state-of-the-art Live Scan and Fingerprinting services. Our expert team delivers precise and swift identity verification to meet your unique needs.",
        "address1": "4740 Green River Rd.",
        "address2": "Suite# 105",
        "stateCountry": "CA",
        "city": "Corona",
        "postalCode": "92878",
        "county": "Riverside",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -117.660699,
        "latitude": 33.877170,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T07:00:00-07:00",
                "timeLunch": "2000-01-01T12:00:00-08:00",
                "timeResume": "2000-01-01T13:30:00-07:00",
                "timeClose": "2000-01-01T15:00:00-07:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-07-10T07:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00-08:00",
                "timeResume": "2000-01-01T13:30:00-08:00",
                "timeClose": "2000-01-01T15:00:00-07:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-07-10T07:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00-08:00",
                "timeResume": "2000-01-01T13:30:00-08:00",
                "timeClose": "2000-01-01T15:00:00-07:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-07-10T07:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00-08:00",
                "timeResume": "2000-01-01T13:30:00-08:00",
                "timeClose": "2000-01-01T15:00:00-07:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T07:00:00-07:00",
                "timeLunch": "2000-01-01T12:00:00-07:00",
                "timeResume": "2000-01-01T13:30:00-07:00",
                "timeClose": "2000-01-01T15:00:00-07:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "08a0c044-9dbe-ed11-a8de-6045bdee2d76",
        "name": "At Your Service WCQ LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Atlanta, GA",
        "description": None,
        "metaDescription": "Explore PrintScan in Atlanta, Georgia, the premier destination for advanced Live Scan and Fingerprinting services. We provide secure, swift, and dependable solutions, making us your go-to choice for all identification needs.",
        "notes": "Explore PrintScan in Atlanta, Georgia, the premier destination for advanced Live Scan and Fingerprinting services. We provide secure, swift, and dependable solutions, making us your go-to choice for all identification needs.",
        "address1": "2247 Godby Rd.",
        "address2": "Suite 107",
        "stateCountry": "GA",
        "city": "Atlanta",
        "postalCode": "30349",
        "county": "Clayton",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -84.463212,
        "latitude": 33.616888,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T13:45:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:30:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T13:45:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:30:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T13:45:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:30:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "1ddc356d-b6c1-ed11-a8de-6045bdee2d76",
        "name": "Drug & Alcohol Testing of Georgia",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Dublin, GA",
        "description": "Across the street from Popeyes in the Kroger shopping center.",
        "metaDescription": "Experience unparalleled Live Scan and Fingerprinting services at PrintScan in Dublin, Georgia. Our dedicated professionals deliver precise and quick results, meeting all your identification requirements. Choose PrintScan Dublin for your trusted and efficient fingerprinting needs.",
        "notes": "Experience unparalleled Live Scan and Fingerprinting services at PrintScan in Dublin, Georgia. Our dedicated professionals deliver precise and quick results, meeting all your identification requirements. Choose PrintScan Dublin for your trusted and efficient fingerprinting needs.",
        "address1": "1022 Hillcrest Pkwy",
        "address2": "Suite 200",
        "stateCountry": "GA",
        "city": "Dublin",
        "postalCode": "31021",
        "county": "Laurens",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -82.934988,
        "latitude": 32.546206,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-03-13T08:00:00+00:00",
                "timeLunch": "2023-03-13T11:00:00+00:00",
                "timeResume": "2023-03-13T12:30:00+00:00",
                "timeClose": "2023-03-13T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-03-13T08:00:00+00:00",
                "timeLunch": "2023-03-13T11:00:00+00:00",
                "timeResume": "2023-03-13T12:30:00+00:00",
                "timeClose": "2023-03-13T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-03-13T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-13T12:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-03-13T08:00:00+00:00",
                "timeLunch": "2023-03-13T11:00:00+00:00",
                "timeResume": "2023-03-13T12:30:00+00:00",
                "timeClose": "2023-03-13T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-03-13T08:00:00+00:00",
                "timeLunch": "2023-03-13T11:00:00+00:00",
                "timeResume": "2023-03-13T12:30:00+00:00",
                "timeClose": "2023-03-13T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b522ca2c-76c2-ed11-a8de-6045bdee2d76",
        "name": "ARCpoint Labs of Atlanta-Northeast",
        "displayName": "Printscan Authorized Fingerprint Service Center - Duluth, GA",
        "description": "Near the intersection of Pleasant Hill Rd. & Peachtree Industrial Blvd.",
        "metaDescription": "Experience top-notch Live Scan and Fingerprinting services at PrintScan in Duluth, Georgia. Your security is our priority with our advanced and reliable identity verification solutions.",
        "notes": "Experience top-notch Live Scan and Fingerprinting services at PrintScan in Duluth, Georgia. Your security is our priority with our advanced and reliable identity verification solutions.",
        "address1": "3635 Savannah Place Dr.",
        "address2": "Suite 450-B",
        "stateCountry": "GA",
        "city": "Duluth",
        "postalCode": "30096",
        "county": "Gwinnett",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -84.167370,
        "latitude": 34.002443,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-03-14T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-14T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-03-14T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-14T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-03-14T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-14T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-03-14T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-14T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-03-14T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-14T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "c6290730-7fc2-ed11-a8de-6045bdee2d76",
        "name": "Value Lab LLC",
        "displayName": "Printscan Authorized Fingerprint Service Center - Byron, IL",
        "description": "Right on RTE 2 across from Felkers grocery store",
        "metaDescription": "Explore superior Live Scan and Fingerprinting services at PrintScan in Byron, Illinois. Our skilled team provides fast, accurate, and dependable results for all your identification needs. Rely on PrintScan Byron for secure and effective fingerprinting solutions.",
        "notes": "Explore superior Live Scan and Fingerprinting services at PrintScan in Byron, Illinois. Our skilled team provides fast, accurate, and dependable results for all your identification needs. Rely on PrintScan Byron for secure and effective fingerprinting solutions.",
        "address1": "404 W Blackhawk Dr",
        "address2": "Ste 101",
        "stateCountry": "IL",
        "city": "Byron",
        "postalCode": "61010",
        "county": "Ogle",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -89.260597,
        "latitude": 42.125044,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-03-14T07:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-14T15:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-03-14T07:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-14T15:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-03-14T07:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-14T15:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-03-14T07:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-14T15:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-03-14T07:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-14T15:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "542073ea-81c2-ed11-a8de-6045bdee2d76",
        "name": "Titan Medical Center",
        "displayName": "Printscan Authorized Fingerprint Service Center - Wichita, KS",
        "description": None,
        "metaDescription": "Discover PrintScan in Wichita, KS - your trusted destination for high-quality Live Scan and Fingerprinting services. Experience fast, secure, and reliable solutions tailored to your needs.",
        "notes": "Discover PrintScan in Wichita, KS - your trusted destination for high-quality Live Scan and Fingerprinting services. Experience fast, secure, and reliable solutions tailored to your needs.",
        "address1": "1415 West 31st St",
        "address2": None,
        "stateCountry": "KS",
        "city": "Wichita",
        "postalCode": "67217",
        "county": "Sedgwick",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -97.356024,
        "latitude": 37.636377,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-03-14T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-14T13:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-03-14T14:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-14T18:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-03-14T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-14T13:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-03-14T14:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-14T18:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-03-14T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-14T13:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "6bfbd601-90c2-ed11-a8de-6045bdee2d76",
        "name": "A Chance to Change Drug & Alc Testing",
        "displayName": "Printscan Authorized Fingerprint Service Center - Caro, MI",
        "description": "South East corner of state st and burnside. A block west of the courthouse",
        "metaDescription": "Get access to exceptional Live Scan and Fingerprinting services at PrintScan in Caro, Michigan. Our proficient team guarantees swift, precise, and reliable results for your identification requirements. Choose PrintScan Caro for trustworthy and efficient fingerprinting solutions.",
        "notes": "Get access to exceptional Live Scan and Fingerprinting services at PrintScan in Caro, Michigan. Our proficient team guarantees swift, precise, and reliable results for your identification requirements. Choose PrintScan Caro for trustworthy and efficient fingerprinting solutions.",
        "address1": "302 N State St",
        "address2": None,
        "stateCountry": "MI",
        "city": "Caro",
        "postalCode": "48723",
        "county": "Tuscola",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -83.394317,
        "latitude": 43.490246,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-03-14T07:00:00+00:00",
                "timeLunch": "2023-03-14T10:00:00+00:00",
                "timeResume": "2023-03-14T13:30:00+00:00",
                "timeClose": "2023-03-14T17:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-03-14T07:00:00+00:00",
                "timeLunch": "2023-03-14T10:00:00+00:00",
                "timeResume": "2023-03-14T13:30:00+00:00",
                "timeClose": "2023-03-14T17:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-03-14T07:00:00+00:00",
                "timeLunch": "2023-03-14T10:00:00+00:00",
                "timeResume": "2023-03-14T13:30:00+00:00",
                "timeClose": "2023-03-14T17:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-03-14T07:00:00+00:00",
                "timeLunch": "2023-03-14T10:00:00+00:00",
                "timeResume": "2023-03-14T13:30:00+00:00",
                "timeClose": "2023-03-14T17:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-03-14T07:00:00+00:00",
                "timeLunch": "2023-03-14T10:00:00+00:00",
                "timeResume": "2023-03-14T13:30:00+00:00",
                "timeClose": "2023-03-14T17:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "627af85c-30c3-ed11-a8de-6045bdee2d76",
        "name": "Infinite Services LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Parsippany, NJ",
        "description": "For special accommodations please email: infiniteservicesllc01@gmail.com",
        "metaDescription": "Experience the best in Live Scan and Fingerprinting services at PrintScan in Parsippany, New Jersey. Our dedicated team delivers quick, accurate, and trustworthy results for all your identification needs. Count on PrintScan Parsippany for secure and efficient fingerprinting solutions.",
        "notes": "Experience the best in Live Scan and Fingerprinting services at PrintScan in Parsippany, New Jersey. Our dedicated team delivers quick, accurate, and trustworthy results for all your identification needs. Count on PrintScan Parsippany for secure and efficient fingerprinting solutions.",
        "address1": "1130 US Highway 46",
        "address2": "Suite 5",
        "stateCountry": "NJ",
        "city": "Parsippany",
        "postalCode": "07054",
        "county": "Morris",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -74.386925,
        "latitude": 40.863432,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "86264373-32c3-ed11-a8de-6045bdee2d76",
        "name": "ARCpoint Labs of Fayetteville, NC",
        "displayName": "Printscan Authorized Fingerprint Service Center - Fayetteville, NC",
        "description": None,
        "metaDescription": "Choose PrintScan in Fayetteville, North Carolina for top-tier Live Scan and Fingerprinting services. Our dedicated team provides fast and accurate identification solutions. Rely on PrintScan Fayetteville, NC for all your secure fingerprinting requirements.",
        "notes": "Choose PrintScan in Fayetteville, North Carolina for top-tier Live Scan and Fingerprinting services. Our dedicated team provides fast and accurate identification solutions. Rely on PrintScan Fayetteville, NC for all your secure fingerprinting requirements.",
        "address1": "605 South Reilly Rd",
        "address2": None,
        "stateCountry": "NC",
        "city": "Fayetteville",
        "postalCode": "28314",
        "county": "Cumberland",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -79.012897,
        "latitude": 35.066101,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-04T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-04T15:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-04T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-04T15:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-04T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-04T15:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-04T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-04T15:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-04T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-04T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "2857cf04-38c3-ed11-a8de-6045bdee2d76",
        "name": "ARCpoint Labs of Jacksonville, NC",
        "displayName": "Printscan Authorized Fingerprint Service Center - Jacksonville, NC",
        "description": None,
        "metaDescription": "Discover premium Live Scan and Fingerprinting services at PrintScan in Jacksonville, North Carolina. Our expert team ensures fast, precise, and reliable results for all your identification requirements. Trust PrintScan Jacksonville for your secure and effective fingerprinting needs.",
        "notes": "Discover premium Live Scan and Fingerprinting services at PrintScan in Jacksonville, North Carolina. Our expert team ensures fast, precise, and reliable results for all your identification requirements. Trust PrintScan Jacksonville for your secure and effective fingerprinting needs.",
        "address1": "3221 Henderson Drive",
        "address2": None,
        "stateCountry": "NC",
        "city": "Jacksonville",
        "postalCode": "28546",
        "county": "Onslow",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -77.418713,
        "latitude": 34.791551,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-17T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-17T15:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-17T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-17T15:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-17T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-17T15:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-17T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-17T15:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-17T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-17T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "c9afd4d7-39c3-ed11-a8de-6045bdee2d76",
        "name": "Eastern Carolina Drug Screen",
        "displayName": "Printscan Authorized Fingerprint Service Center - Rocky Mount, NC",
        "description": None,
        "metaDescription": "Choose PrintScan in Rocky Mount, North Carolina for all your Live Scan and Fingerprinting needs. Our dedicated team delivers high-quality, efficient identification services you can trust.",
        "notes": "Choose PrintScan in Rocky Mount, North Carolina for all your Live Scan and Fingerprinting needs. Our dedicated team delivers high-quality, efficient identification services you can trust.",
        "address1": "3208 Sunset Ave",
        "address2": None,
        "stateCountry": "NC",
        "city": "Rocky Mount",
        "postalCode": "27804",
        "county": "Nash",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -77.842669,
        "latitude": 35.963662,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-10T08:30:00+00:00",
                "timeLunch": "2023-08-10T11:00:00+00:00",
                "timeResume": "2023-08-10T12:30:00+00:00",
                "timeClose": "2023-08-10T15:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-10T08:30:00+00:00",
                "timeLunch": "2023-08-10T11:00:00+00:00",
                "timeResume": "2023-08-10T12:30:00+00:00",
                "timeClose": "2023-08-10T15:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-10T08:30:00+00:00",
                "timeLunch": "2023-08-10T11:00:00+00:00",
                "timeResume": "2023-08-10T12:30:00+00:00",
                "timeClose": "2023-08-10T15:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-10T08:30:00+00:00",
                "timeLunch": "2023-08-10T11:00:00+00:00",
                "timeResume": "2023-08-10T12:30:00+00:00",
                "timeClose": "2023-08-10T15:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T11:30:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "89d463de-40c3-ed11-a8de-6045bdee2d76",
        "name": "ARCpoint Labs of Columbus Metro",
        "displayName": "Printscan Authorized Fingerprint Service Center - Columbus, OH",
        "description": None,
        "metaDescription": "Visit PrintScan in Columbus, Ohio for reliable Live Scan and Fingerprinting services. Our team is committed to providing accurate and quick results to meet all your identification needs.",
        "notes": "Visit PrintScan in Columbus, Ohio for reliable Live Scan and Fingerprinting services. Our team is committed to providing accurate and quick results to meet all your identification needs.",
        "address1": "1335 Dublin Rd",
        "address2": "Suite 118E",
        "stateCountry": "OH",
        "city": "Columbus",
        "postalCode": "43215",
        "county": "Franklin",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -83.062829,
        "latitude": 39.979498,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-05-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-23T15:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-05-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-23T15:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-05-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-23T15:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-05-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-23T15:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-05-23T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-23T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "4f965d5c-44c3-ed11-a8de-6045bdee2d76",
        "name": "ARCpoint Labs of Sugar Land, TX",
        "displayName": "Printscan Authorized Fingerprint Service Center - Sugar Land, TX",
        "description": "(ARCpoint Labs) Across Parking Lot from Dynamic Fitness",
        "metaDescription": "Experience the best in Live Scan and Fingerprinting services at PrintScan in Sugar Land, Texas. We provide efficient, secure, and customized identification solutions to meet your unique needs.",
        "notes": "Experience the best in Live Scan and Fingerprinting services at PrintScan in Sugar Land, Texas. We provide efficient, secure, and customized identification solutions to meet your unique needs.",
        "address1": "9920 US-90 ALT A",
        "address2": "Suite 160D",
        "stateCountry": "TX",
        "city": "Sugar Land",
        "postalCode": "77478",
        "county": "Fort Bend",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -95.604456,
        "latitude": 29.624927,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-05-18T08:00:00+00:00",
                "timeLunch": "2023-05-18T11:30:00+00:00",
                "timeResume": "2023-05-18T13:30:00+00:00",
                "timeClose": "2023-05-18T16:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-05-18T08:00:00+00:00",
                "timeLunch": "2023-05-18T11:30:00+00:00",
                "timeResume": "2023-05-18T13:30:00+00:00",
                "timeClose": "2023-05-18T16:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-05-18T08:00:00+00:00",
                "timeLunch": "2023-05-18T11:30:00+00:00",
                "timeResume": "2023-05-18T13:30:00+00:00",
                "timeClose": "2023-05-18T16:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-05-18T08:00:00+00:00",
                "timeLunch": "2023-05-18T11:30:00+00:00",
                "timeResume": "2023-05-18T13:30:00+00:00",
                "timeClose": "2023-05-18T16:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-05-18T08:00:00+00:00",
                "timeLunch": "2023-05-18T11:30:00+00:00",
                "timeResume": "2023-05-18T13:30:00+00:00",
                "timeClose": "2023-05-18T16:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "a35513de-f9c3-ed11-a8de-6045bdee2d76",
        "name": "ARCpoint Labs of Orland Park, IL",
        "displayName": "Printscan Authorized Fingerprint Service Center - Orland Park, IL",
        "description": "On 179th in the same plaza with Subway & LI House Chinese",
        "metaDescription": "Experience unmatched Live Scan and Fingerprinting services at PrintScan in Orland Park, Illinois. Our dedicated team delivers fast, precise, and reliable results for your identification requirements. Choose PrintScan Orland Park for your trusted and efficient fingerprinting needs.",
        "notes": "Experience unmatched Live Scan and Fingerprinting services at PrintScan in Orland Park, Illinois. Our dedicated team delivers fast, precise, and reliable results for your identification requirements. Choose PrintScan Orland Park for your trusted and efficient fingerprinting needs.",
        "address1": "11006 W 179th Street",
        "address2": None,
        "stateCountry": "IL",
        "city": "Orland Park",
        "postalCode": "60467",
        "county": "Cook",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -87.887223,
        "latitude": 41.564711,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-10T08:00:00+00:00",
                "timeLunch": "2023-08-10T12:00:00+00:00",
                "timeResume": "2023-08-10T13:00:00+00:00",
                "timeClose": "2023-08-10T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-10T08:00:00+00:00",
                "timeLunch": "2023-08-10T12:00:00+00:00",
                "timeResume": "2023-08-10T13:00:00+00:00",
                "timeClose": "2023-08-10T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-10T10:00:00+00:00",
                "timeLunch": "2023-08-10T14:00:00+00:00",
                "timeResume": "2023-08-10T15:00:00+00:00",
                "timeClose": "2023-08-10T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-10T08:00:00+00:00",
                "timeLunch": "2023-08-10T12:00:00+00:00",
                "timeResume": "2023-08-10T13:00:00+00:00",
                "timeClose": "2023-08-10T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-10T08:00:00+00:00",
                "timeLunch": "2023-08-10T12:00:00+00:00",
                "timeResume": "2023-08-10T13:00:00+00:00",
                "timeClose": "2023-08-10T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "209788ae-ffc3-ed11-a8de-6045bdee2d76",
        "name": "ARCpoint Labs of San Antonio West Medical",
        "displayName": "Printscan Authorized Fingerprint Service Center - San Antonio, TX",
        "description": "Hubner Tech Center",
        "metaDescription": "Visit PrintScan in San Antonio, Texas, your reliable source for high-quality Live Scan and Fingerprinting services. We provide fast, secure, and trusted solutions to meet all your identification and verification needs.",
        "notes": "Visit PrintScan in San Antonio, Texas, your reliable source for high-quality Live Scan and Fingerprinting services. We provide fast, secure, and trusted solutions to meet all your identification and verification needs.",
        "address1": "8666 Huebner Rd",
        "address2": "Suite 102",
        "stateCountry": "TX",
        "city": "San Antonio",
        "postalCode": "78240",
        "county": "Bexar",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -98.601379,
        "latitude": 29.521215,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-03-16T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-16T16:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-03-16T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-16T16:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-03-16T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-16T16:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-03-16T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-16T16:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-03-16T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-16T16:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "0e2eba5d-01c4-ed11-a8de-6045bdee2d76",
        "name": "ARCpoint Labs of Milwaukee North",
        "displayName": "Printscan Authorized Fingerprint Service Center - Brookfield, WI",
        "description": "Across the street from  home depot. Near corner of 12th St and Capital Ave.",
        "metaDescription": "Discover exceptional Live Scan and Fingerprinting services at PrintScan in Brookfield, Wisconsin. Our expert team ensures fast, precise, and reliable results for your identification requirements. Choose PrintScan Brookfield for your trusted and efficient fingerprinting needs.",
        "notes": "Discover exceptional Live Scan and Fingerprinting services at PrintScan in Brookfield, Wisconsin. Our expert team ensures fast, precise, and reliable results for your identification requirements. Choose PrintScan Brookfield for your trusted and efficient fingerprinting needs.",
        "address1": "4125 N 124th Street",
        "address2": "Suite G",
        "stateCountry": "WI",
        "city": "Brookfield",
        "postalCode": "53005",
        "county": "Waukesha",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -88.066915,
        "latitude": 43.091874,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-04-17T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-17T16:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-04-17T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-17T16:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-04-17T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-17T16:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-04-17T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-17T16:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-04-17T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-17T16:30:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-04-17T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-17T11:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "9b4f6588-07c4-ed11-a8de-6045bdee2d76",
        "name": "ARCpoint Labs of Dunnellon",
        "displayName": "Printscan Authorized Fingerprint Service Center - Ocala, FL",
        "description": "Located inside Dunnellon Pharmacy",
        "metaDescription": "Explore superior Live Scan and Fingerprinting services at PrintScan in Dunnellon, Florida. Our skilled team provides fast, accurate, and dependable results for all your identification requirements. Trust PrintScan Dunnellon for your secure and effective fingerprinting needs.",
        "notes": "Explore superior Live Scan and Fingerprinting services at PrintScan in Dunnellon, Florida. Our skilled team provides fast, accurate, and dependable results for all your identification requirements. Trust PrintScan Dunnellon for your secure and effective fingerprinting needs.",
        "address1": "11150 N Willims St",
        "address2": "101B",
        "stateCountry": "FL",
        "city": "Dunnellon",
        "postalCode": "34432",
        "county": "Marion",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -82.455008,
        "latitude": 29.061771,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "a1c74e63-0cc4-ed11-a8de-6045bdee2d76",
        "name": "ARCpoint Labs of Irving, TX",
        "displayName": "Printscan Authorized Fingerprint Service Center - Irving, TX",
        "description": None,
        "metaDescription": "Choose PrintScan Irving, Texas for top-tier Live Scan and Fingerprinting services. Our expert team is committed to providing fast and accurate identification solutions. Rely on PrintScan Irving for all your fingerprinting needs.",
        "notes": "Choose PrintScan Irving, Texas for top-tier Live Scan and Fingerprinting services. Our expert team is committed to providing fast and accurate identification solutions. Rely on PrintScan Irving for all your fingerprinting needs.",
        "address1": "8925 Sterling Street",
        "address2": "Suite 255",
        "stateCountry": "TX",
        "city": "Irving",
        "postalCode": "75063",
        "county": "Dallas",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -97.017655,
        "latitude": 32.929747,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-03-16T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-16T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-03-16T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-16T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-03-16T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-16T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-03-16T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-16T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-03-16T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-16T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "5976f58e-10c4-ed11-a8de-6045bdee2d76",
        "name": "ARCpoint Labs of Greenville, NC",
        "displayName": "Printscan Authorized Fingerprint Service Center - Greenville, NC",
        "description": None,
        "metaDescription": "Discover top-notch Live Scan and Fingerprinting solutions at PrintScan in Greenville, North Carolina. We prioritize your security with our high-quality, efficient identification services.",
        "notes": "Discover top-notch Live Scan and Fingerprinting solutions at PrintScan in Greenville, North Carolina. We prioritize your security with our high-quality, efficient identification services.",
        "address1": "2780 Dickinson Avenue",
        "address2": "Suite B",
        "stateCountry": "NC",
        "city": "Greenville",
        "postalCode": "27834",
        "county": "Pitt",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -77.405575,
        "latitude": 35.593163,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-03T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-03T15:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-03T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-03T15:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-14T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-14T16:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-03T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-03T15:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-03T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-03T15:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "af868017-12c4-ed11-a8de-6045bdee2d76",
        "name": "ARCpoint Labs of New Bern, NC",
        "displayName": "Printscan Authorized Fingerprint Service Center - New Bern, NC",
        "description": None,
        "metaDescription": "Get access to premium Live Scan and Fingerprinting services at PrintScan in New Bern, North Carolina. Our proficient team guarantees swift, precise, and reliable results for your identification needs. Choose PrintScan New Bern for trustworthy and efficient fingerprinting solutions.",
        "notes": "Get access to premium Live Scan and Fingerprinting services at PrintScan in New Bern, North Carolina. Our proficient team guarantees swift, precise, and reliable results for your identification needs. Choose PrintScan New Bern for trustworthy and efficient fingerprinting solutions.",
        "address1": "2500 Trent Road",
        "address2": "Suite 34",
        "stateCountry": "NC",
        "city": "New Bern",
        "postalCode": "28562",
        "county": "Craven",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -77.079785,
        "latitude": 35.099715,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-04T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-04T15:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-04T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-04T15:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-04T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-04T15:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-04T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-04T15:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-04T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-04T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "657b1b0b-15c4-ed11-a8de-6045bdee2d76",
        "name": "ARCpoint Labs of Tipp City",
        "displayName": "Printscan Authorized Fingerprint Service Center - Tipp City, OH",
        "description": "4th suite in the Tipp City Professional Building",
        "metaDescription": "Choose PrintScan in Tipp City, Ohio for top-tier Live Scan and Fingerprinting services. We're dedicated to offering secure, fast, and reliable identification solutions tailored to your needs.",
        "notes": "Choose PrintScan in Tipp City, Ohio for top-tier Live Scan and Fingerprinting services. We're dedicated to offering secure, fast, and reliable identification solutions tailored to your needs.",
        "address1": "1487 West Main Street",
        "address2": None,
        "stateCountry": "OH",
        "city": "Tipp City",
        "postalCode": "45371",
        "county": "Miami",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -84.197734,
        "latitude": 39.963039,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-07T09:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00-04:00",
                "timeResume": "2000-01-01T13:00:00-04:00",
                "timeClose": "2000-01-01T15:15:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-07T09:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00-04:00",
                "timeResume": "2000-01-01T13:00:00-04:00",
                "timeClose": "2000-01-01T15:15:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-07T09:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00-04:00",
                "timeResume": "2000-01-01T13:00:00-04:00",
                "timeClose": "2000-01-01T15:15:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-07T09:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00-04:00",
                "timeResume": "2000-01-01T13:00:00-04:00",
                "timeClose": "2000-01-01T15:15:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-07T09:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00-04:00",
                "timeResume": "2000-01-01T13:00:00-04:00",
                "timeClose": "2000-01-01T15:15:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "4e6ab1f3-c9c4-ed11-a8de-6045bdee2d76",
        "name": "Vault Logistics and Diagnostics LLC",
        "displayName": "Printscan Authorized Fingerprint Service Center - Winterhaven, FL",
        "description": None,
        "metaDescription": "Rely on PrintScan in Winter Haven, Florida for high-quality Live Scan and Fingerprinting services. Our expert team ensures quick and accurate results for your identification requirements.",
        "notes": "Rely on PrintScan in Winter Haven, Florida for high-quality Live Scan and Fingerprinting services. Our expert team ensures quick and accurate results for your identification requirements.",
        "address1": "65 3rd St. NW",
        "address2": "Suite 203",
        "stateCountry": "FL",
        "city": "Winter Haven",
        "postalCode": "33881",
        "county": "Polk",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.730546,
        "latitude": 28.022891,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T07:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T07:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T07:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "a77d44bc-f3c7-ed11-a8de-6045bdee2d76",
        "name": "ARCpoint Labs of Santa Fe Springs, CA",
        "displayName": "Printscan Authorized Fingerprint Service Center - Santa Fe Springs, CA",
        "description": None,
        "metaDescription": "Discover top-notch Live Scan and Fingerprinting services at PrintScan in Santa Fe Springs, California. We prioritize accuracy and efficiency in every service we provide. Choose PrintScan Santa Fe Springs for your identification requirements.",
        "notes": "Discover top-notch Live Scan and Fingerprinting services at PrintScan in Santa Fe Springs, California. We prioritize accuracy and efficiency in every service we provide. Choose PrintScan Santa Fe Springs for your identification requirements.",
        "address1": "8620 Sorenson Avenue",
        "address2": "Suite 4",
        "stateCountry": "CA",
        "city": "Santa Fe Springs",
        "postalCode": "90670",
        "county": "Los Angeles",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -118.060164,
        "latitude": 33.962536,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-06-09T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-09T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-06-09T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-09T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-06-09T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-09T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-06-09T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-09T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-06-09T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-09T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "22791dbd-f7c7-ed11-a8de-6045bdee2d76",
        "name": "Forward Edge",
        "displayName": "Printscan Authorized Fingerprint Service Center - Frankfort, KY",
        "description": None,
        "metaDescription": "Get superior Live Scan and Fingerprinting services at PrintScan in Frankfort, Kentucky. Our commitment to precision and speed sets us apart. Rely on PrintScan Frankfort for all your identification needs.",
        "notes": "Get superior Live Scan and Fingerprinting services at PrintScan in Frankfort, Kentucky. Our commitment to precision and speed sets us apart. Rely on PrintScan Frankfort for all your identification needs.",
        "address1": "859 E Main St",
        "address2": "Ste 2c",
        "stateCountry": "KY",
        "city": "Frankfort",
        "postalCode": "40601",
        "county": "Franklin",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -84.839882,
        "latitude": 38.204232,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-04-18T13:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-18T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-04-18T13:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-04-18T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "2e42f474-b5c8-ed11-a8de-6045bdee2d76",
        "name": "ARCpoint Labs of Cincinnati East",
        "displayName": "Printscan Authorized Fingerprint Service Center -  Cincinnati, OH",
        "description": "Located inside EASTGATE PROFESSIONAL OFFICE PARK - After you enter the lobby, go straight back, turn and go down the hallway on the left. We are the last door on the right.",
        "metaDescription": "Discover top-notch Live Scan and Fingerprinting services in Cincinnati, Ohio at PrintScan. We offer efficient, secure, and professional identification solutions tailored to your specific needs.",
        "notes": "Discover top-notch Live Scan and Fingerprinting services in Cincinnati, Ohio at PrintScan. We offer efficient, secure, and professional identification solutions tailored to your specific needs.",
        "address1": "4357 Ferguson Dr",
        "address2": "Suite 130",
        "stateCountry": "OH",
        "city": "Cincinnati",
        "postalCode": "45245",
        "county": "Clermont",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -84.282887,
        "latitude": 39.093840,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-03-22T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-22T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-03-22T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-22T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-03-22T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-22T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-03-22T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-22T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-03-22T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-22T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b8e5071b-b6c8-ed11-a8de-6045bdee2d76",
        "name": "ADAT Inc",
        "displayName": "Printscan Authorized Fingerprint Service Center - San Diego, Ca",
        "description": None,
        "metaDescription": "Explore PrintScan in San Diego, California for comprehensive Live Scan and Fingerprinting services. We provide swift, accurate, and professional solutions to meet your identification needs.",
        "notes": "Explore PrintScan in San Diego, California for comprehensive Live Scan and Fingerprinting services. We provide swift, accurate, and professional solutions to meet your identification needs.",
        "address1": "2667 Camino del Rio S",
        "address2": "Ste 100h",
        "stateCountry": "CA",
        "city": "San Diego",
        "postalCode": "92108",
        "county": "San Diego",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -117.135161,
        "latitude": 32.769083,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-07-10T08:00:00+00:00",
                "timeLunch": "2023-07-10T12:00:00+00:00",
                "timeResume": "2023-07-10T13:00:00+00:00",
                "timeClose": "2023-07-10T16:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-07-10T08:00:00+00:00",
                "timeLunch": "2023-07-10T12:00:00+00:00",
                "timeResume": "2023-07-10T13:00:00+00:00",
                "timeClose": "2023-07-10T16:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-07-10T08:00:00+00:00",
                "timeLunch": "2023-07-10T12:00:00+00:00",
                "timeResume": "2023-07-10T13:00:00+00:00",
                "timeClose": "2023-07-10T16:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-07-10T08:00:00+00:00",
                "timeLunch": "2023-07-10T12:00:00+00:00",
                "timeResume": "2023-07-10T13:00:00+00:00",
                "timeClose": "2023-07-10T16:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-07-10T08:00:00+00:00",
                "timeLunch": "2023-07-10T12:00:00+00:00",
                "timeResume": "2023-07-10T13:00:00+00:00",
                "timeClose": "2023-07-10T16:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "440261ed-b8c8-ed11-a8de-6045bdee2d76",
        "name": "ARCpoint Labs of Downtown Fort Worth, TX",
        "displayName": "Printscan Authorized Fingerprint Service Center - Fort Worth, TX",
        "description": None,
        "metaDescription": "Visit PrintScan in Fort Worth, Texas, for exceptional Live Scan and Fingerprinting services. Our expert team guarantees accuracy and quick turnaround times. Trust in PrintScan Fort Worth for all your identification solutions.",
        "notes": "Visit PrintScan in Fort Worth, Texas, for exceptional Live Scan and Fingerprinting services. Our expert team guarantees accuracy and quick turnaround times. Trust in PrintScan Fort Worth for all your identification solutions.",
        "address1": "2757 Airport Freeway",
        "address2": None,
        "stateCountry": "TX",
        "city": "Fort Worth",
        "postalCode": "76111",
        "county": "Tarrant",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -97.306276,
        "latitude": 32.768105,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-03-22T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-22T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-03-22T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-22T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-03-22T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-22T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-03-22T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-22T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-03-22T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-22T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b0920d91-bdc8-ed11-a8de-6045bdee2d76",
        "name": "ARCpoint Labs of Portsmouth, VA",
        "displayName": "Printscan Authorized Fingerprint Service Center - Portsmouth, VA",
        "description": None,
        "metaDescription": "Experience unparalleled Live Scan and Fingerprinting services at PrintScan in Portsmouth, Virginia. We pride ourselves on our accuracy and efficiency. Choose PrintScan Portsmouth for all your identification service needs.",
        "notes": "Experience unparalleled Live Scan and Fingerprinting services at PrintScan in Portsmouth, Virginia. We pride ourselves on our accuracy and efficiency. Choose PrintScan Portsmouth for all your identification service needs.",
        "address1": "742 Florida Avenue",
        "address2": None,
        "stateCountry": "VA",
        "city": "Portsmouth",
        "postalCode": "23707",
        "county": "Portsmouth City",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -76.337512,
        "latitude": 36.841532,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-03-22T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-22T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-03-22T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-22T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-03-22T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-22T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-03-22T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-22T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-03-22T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-22T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "c4561cf9-dac8-ed11-a8de-6045bdee2d76",
        "name": "ARCpoint Labs of Florence, KY",
        "displayName": "Printscan Authorized Fingerprint Service Center - Florence, KY",
        "description": None,
        "metaDescription": "Visit PrintScan in Florence, Kentucky, for high-quality Live Scan and Fingerprinting services. Our team ensures accuracy and speed in every service we provide. Trust PrintScan Florence for all your identification needs.",
        "notes": "Visit PrintScan in Florence, Kentucky, for high-quality Live Scan and Fingerprinting services. Our team ensures accuracy and speed in every service we provide. Trust PrintScan Florence for all your identification needs.",
        "address1": "8174 Mall Road",
        "address2": None,
        "stateCountry": "KY",
        "city": "Florence",
        "postalCode": "41042",
        "county": "Boone",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -84.649404,
        "latitude": 38.983111,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-03-22T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-22T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-03-22T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-22T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-03-22T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-22T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-03-22T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-22T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-03-22T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-03-22T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "da0408fc-9cc9-ed11-a8de-6045bdee2d76",
        "name": "Helping Hands Superior Care LLC",
        "displayName": "PrintScan Authorized Service Center - New Port Richey, FL",
        "description": "Next to Sam's club, Double doors Entrance",
        "metaDescription": "Rely on PrintScan in New Port Richey, Florida for top-notch Live Scan and Fingerprinting services. Our professional team ensures a seamless and efficient process for all your identification needs.",
        "notes": "Rely on PrintScan in New Port Richey, Florida for top-notch Live Scan and Fingerprinting services. Our professional team ensures a seamless and efficient process for all your identification needs.",
        "address1": "5006 Trouble Creek Road Suite #228",
        "address2": "Suite #228",
        "stateCountry": "FL",
        "city": "New Port Richey",
        "postalCode": "34652",
        "county": "Pasco",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -82.731430,
        "latitude": 28.223996,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 0,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-05:00"
            },
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-06-02T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-06-02T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "9d9093fe-c9cc-ed11-a8de-6045bdee2d76",
        "name": "RHTC Medical LLC",
        "displayName": "Printscan Authorized Fingerprint Service Center - Florence, SC",
        "description": "Across from Sexton Dental Clinic",
        "metaDescription": "Trust PrintScan in Florence, South Carolina for high-quality Live Scan and Fingerprinting services. Our state-of-the-art technology and experienced team are here to provide secure and efficient solutions. Visit us today for your needs!",
        "notes": "Trust PrintScan in Florence, South Carolina for high-quality Live Scan and Fingerprinting services. Our state-of-the-art technology and experienced team are here to provide secure and efficient solutions. Visit us today for your needs!",
        "address1": "376 West Palmetto Street",
        "address2": None,
        "stateCountry": "SC",
        "city": "Florence",
        "postalCode": "29501",
        "county": "Florence",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -79.771815,
        "latitude": 34.193239,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:00:00-04:00",
                "timeLunch": "2000-01-01T11:45:00-04:00",
                "timeResume": "2000-01-01T13:00:00-04:00",
                "timeClose": "2000-01-01T15:45:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:00:00-04:00",
                "timeLunch": "2000-01-01T11:45:00-04:00",
                "timeResume": "2000-01-01T13:00:00-04:00",
                "timeClose": "2000-01-01T15:45:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:00:00-04:00",
                "timeLunch": "2000-01-01T11:45:00-04:00",
                "timeResume": "2000-01-01T13:00:00-04:00",
                "timeClose": "2000-01-01T15:45:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:00:00-04:00",
                "timeLunch": "2000-01-01T11:45:00-04:00",
                "timeResume": "2000-01-01T13:00:00-04:00",
                "timeClose": "2000-01-01T15:45:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:00:00-04:00",
                "timeLunch": "2000-01-01T11:45:00-04:00",
                "timeResume": "2000-01-01T13:00:00-04:00",
                "timeClose": "2000-01-01T15:45:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "4ce81da7-71cd-ed11-a8de-6045bdee2d76",
        "name": "Hurst Notary Services",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Munford, TN",
        "description": "Inside the Regency Bank",
        "metaDescription": "Visit PrintScan in Munford, Tennessee, for high-quality Live Scan and Fingerprinting services. Our team ensures accuracy and efficiency in every service we provide. Trust PrintScan Munford for all your identification needs.",
        "notes": "Visit PrintScan in Munford, Tennessee, for high-quality Live Scan and Fingerprinting services. Our team ensures accuracy and efficiency in every service we provide. Trust PrintScan Munford for all your identification needs.",
        "address1": "86 South Tipton Street",
        "address2": "Unit 203",
        "stateCountry": "TN",
        "city": "Munford",
        "postalCode": "38058",
        "county": "Tipton",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -89.814612,
        "latitude": 35.447400,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "bfea3056-76cd-ed11-a8de-6045bdee2d76",
        "name": "Genesis Testing Solutions",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Mobile, AL",
        "description": None,
        "metaDescription": "Discover PrintScan Mobile, Alabama, your reliable provider for Live Scan and Fingerprinting services. We offer efficient, accurate, and secure identification solutions tailored to meet your specific needs.",
        "notes": "Discover PrintScan Mobile, Alabama, your reliable provider for Live Scan and Fingerprinting services. We offer efficient, accurate, and secure identification solutions tailored to meet your specific needs.",
        "address1": "1111 East I-65 Service Road South, Suite 104",
        "address2": None,
        "stateCountry": "AL",
        "city": "Mobile",
        "postalCode": "36606",
        "county": "Mobile",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -88.126480,
        "latitude": 30.667621,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "76b24219-77cd-ed11-a8de-6045bdee2d76",
        "name": "Heart To Home Healthcare Services Inc",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Memphis, TN 38116",
        "description": None,
        "metaDescription": "Choose PrintScan in Memphis, Tennessee for reliable Live Scan and Fingerprinting services. We are committed to delivering accurate, secure, and quick identity solutions, prioritizing your safety and satisfaction.",
        "notes": "Choose PrintScan in Memphis, Tennessee for reliable Live Scan and Fingerprinting services. We are committed to delivering accurate, secure, and quick identity solutions, prioritizing your safety and satisfaction.",
        "address1": "1703 Bender Road",
        "address2": None,
        "stateCountry": "TN",
        "city": "Memphis",
        "postalCode": "38116",
        "county": "Shelby",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -90.006972,
        "latitude": 35.019044,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "e0ab9151-95cd-ed11-a8de-6045bdee2d76",
        "name": "Hazon Screening",
        "displayName": "Printscan Authorized Fingerprint Service Center - Baton Rouge, LA",
        "description": None,
        "metaDescription": "Visit PrintScan in Baton Rouge, Louisiana, for superior Live Scan and Fingerprinting services. We provide fast, secure, and personalized identification solutions to meet your unique requirements.",
        "notes": "Visit PrintScan in Baton Rouge, Louisiana, for superior Live Scan and Fingerprinting services. We provide fast, secure, and personalized identification solutions to meet your unique requirements.",
        "address1": "2320 Drusilla Lane Suite A",
        "address2": None,
        "stateCountry": "LA",
        "city": "Baton Rouge",
        "postalCode": "70809",
        "county": "East Baton Rouge",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -91.084468,
        "latitude": 30.429214,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-04-12T10:00:00+00:00",
                "timeLunch": "2023-04-12T13:30:00+00:00",
                "timeResume": "2023-04-12T14:00:00+00:00",
                "timeClose": "2023-04-12T15:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-04-12T10:00:00+00:00",
                "timeLunch": "2023-04-12T13:30:00+00:00",
                "timeResume": "2023-04-12T14:00:00+00:00",
                "timeClose": "2023-04-12T15:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-04-12T10:00:00+00:00",
                "timeLunch": "2023-04-12T13:30:00+00:00",
                "timeResume": "2023-04-12T14:00:00+00:00",
                "timeClose": "2023-04-12T15:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-04-12T10:00:00+00:00",
                "timeLunch": "2023-04-12T13:30:00+00:00",
                "timeResume": "2023-04-12T14:00:00+00:00",
                "timeClose": "2023-04-12T15:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-04-12T10:00:00+00:00",
                "timeLunch": "2023-04-12T13:30:00+00:00",
                "timeResume": "2023-04-12T14:00:00+00:00",
                "timeClose": "2023-04-12T15:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "017e7e6c-55ce-ed11-a8de-6045bdee2d76",
        "name": "Blue Star Diagnostics of Plano",
        "displayName": "Printscan Authorized Fingerprint Service Center - Plano, TX",
        "description": None,
        "metaDescription": "Visit PrintScan in Plano, Texas, your trusted destination for superior Live Scan and Fingerprinting services. Take advantage of our speedy, secure, and custom solutions designed to meet your specific needs.",
        "notes": "Visit PrintScan in Plano, Texas, your trusted destination for superior Live Scan and Fingerprinting services. Take advantage of our speedy, secure, and custom solutions designed to meet your specific needs.",
        "address1": "720 E Park Blvd",
        "address2": "Ste 102",
        "stateCountry": "TX",
        "city": "Plano",
        "postalCode": "75074",
        "county": "Collin",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -96.704669,
        "latitude": 33.028921,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-01T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-01T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-01T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-01T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-01T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-01T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-01T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-01T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-01T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-01T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "5624b09f-c9cf-ed11-a8de-6045bdee2d76",
        "name": "State Drug Testing and Occupational Health",
        "displayName": "Printscan Authorized Fingerprint Service Center - Garden City, GA",
        "description": None,
        "metaDescription": "Experience fast and reliable Live Scan and Fingerprinting services at PrintScan in Garden City, Georgia. Our dedicated team ensures accurate results for all your identification needs. Trust PrintScan Garden City, GA for secure and efficient fingerprinting solutions.",
        "notes": "Experience fast and reliable Live Scan and Fingerprinting services at PrintScan in Garden City, Georgia. Our dedicated team ensures accurate results for all your identification needs. Trust PrintScan Garden City, GA for secure and efficient fingerprinting solutions.",
        "address1": "24 W Chatham Ct",
        "address2": None,
        "stateCountry": "GA",
        "city": "Garden City",
        "postalCode": "31408",
        "county": "Chatham",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.157031,
        "latitude": 32.084899,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-09-08T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-08T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-09-08T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-08T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-09-08T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-08T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-09-08T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-08T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-09-08T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-08T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "86ab5375-5712-4800-be3b-61fceabdbbbb",
        "name": "YMCA Arvada (Open Wed)",
        "displayName": "PrintScan | YMCA Arvada (Open Wed) - Arvada, CO",
        "description": "",
        "metaDescription": "Rely on PrintScan in Arvada, Colorado for your Live Scan and Fingerprinting needs. We offer secure, efficient, and high-quality fingerprinting services, ensuring your complete satisfaction.",
        "notes": "Rely on PrintScan in Arvada, Colorado for your Live Scan and Fingerprinting needs. We offer secure, efficient, and high-quality fingerprinting services, ensuring your complete satisfaction.",
        "address1": "6350 Eldridge St",
        "address2": None,
        "stateCountry": "CO",
        "city": "Arvada",
        "postalCode": "80004",
        "county": "Jefferson",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -105.155422,
        "latitude": 39.811857,
        "googlePlaceId": None,
        "referenceId": "75",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "398994d1-c150-4f77-b480-65a5c058cda4",
        "name": "Dolores County School District RE-2J (Open Mon-Thurs)",
        "displayName": "PrintScan | Dolores County School District RE-2J (Open Mon-Thurs) - Dove Creek, CO",
        "description": "#459",
        "metaDescription": "Discover the premier Live Scan and Fingerprinting services in Dove Creek, Colorado with PrintScan. We are committed to providing secure, efficient, and high-quality identification solutions for your needs.",
        "notes": "Discover the premier Live Scan and Fingerprinting services in Dove Creek, Colorado with PrintScan. We are committed to providing secure, efficient, and high-quality identification solutions for your needs.",
        "address1": "425 Main St",
        "address2": None,
        "stateCountry": "CO",
        "city": "Dove Creek",
        "postalCode": "81324",
        "county": "Dolores",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -108.903537,
        "latitude": 37.765998,
        "googlePlaceId": None,
        "referenceId": "110",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b732c8b4-7f17-4a3b-b963-68427f44e69b",
        "name": "Pack & Post",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Longview, TX",
        "description": None,
        "metaDescription": "Explore PrintScan Longview, Texas - your top choice for Live Scan and Fingerprinting services. Take advantage of our quick, reliable, and secure solutions, tailored to address your specific needs.",
        "notes": "Explore PrintScan Longview, Texas - your top choice for Live Scan and Fingerprinting services. Take advantage of our quick, reliable, and secure solutions, tailored to address your specific needs.",
        "address1": "2309 Gilmer Road",
        "address2": None,
        "stateCountry": "TX",
        "city": "Longview",
        "postalCode": "75604",
        "county": "Gregg",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -94.788659,
        "latitude": 32.531105,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:45:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:45:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:45:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:45:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:45:00-05:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T12:30:00-06:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "3c7d3d92-3982-474a-8e6d-695112564c40",
        "name": "Texas RxSolutions and Compounding Pharmacy",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Angleton, TX",
        "description": None,
        "metaDescription": "Experience PrintScan in Angleton, Texas, your go-to source for Live Scan and Fingerprinting services. Utilize our fast, dependable, and customized solutions created to fulfill your specific requirements.",
        "notes": "Experience PrintScan in Angleton, Texas, your go-to source for Live Scan and Fingerprinting services. Utilize our fast, dependable, and customized solutions created to fulfill your specific requirements.",
        "address1": "131 East Hospital Drive",
        "address2": None,
        "stateCountry": "TX",
        "city": "Angleton",
        "postalCode": "77515",
        "county": "Brazoria",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -95.404161,
        "latitude": 29.185545,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-06:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-06:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-06:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-06:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-06:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b1ed7867-3866-463f-902f-6af1303b7a2a",
        "name": "Texas Amaral Group",
        "displayName": "PrintScan Authorized Fingerprint Service Center - El Paso, TX",
        "description": None,
        "metaDescription": "Experience fast and reliable Live Scan and Fingerprinting services in El Paso, Texas with PrintScan. We're committed to providing top-notch security solutions for your identification needs.",
        "notes": "Experience fast and reliable Live Scan and Fingerprinting services in El Paso, Texas with PrintScan. We're committed to providing top-notch security solutions for your identification needs.",
        "address1": "801 N. El Paso Street Suite 150",
        "address2": None,
        "stateCountry": "TX",
        "city": "El Paso",
        "postalCode": "79902",
        "county": "El Paso",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -106.493123,
        "latitude": 31.762148,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "c37d6f70-8af7-4c05-8608-6f3cd1dc7a7c",
        "name": "Las Animas DHS (Open Wed)",
        "displayName": "PrintScan | Las Animas DHS (Open Wed) - Trinidad, CO",
        "description": "",
        "metaDescription": "Experience fast and accurate Live Scan and Fingerprinting services at PrintScan in Trinidad, Colorado. Our dedicated team ensures a seamless process for all your identification needs. Trust PrintScan Trinidad for reliable service.",
        "notes": "Experience fast and accurate Live Scan and Fingerprinting services at PrintScan in Trinidad, Colorado. Our dedicated team ensures a seamless process for all your identification needs. Trust PrintScan Trinidad for reliable service.",
        "address1": "219 S Chestnut St",
        "address2": None,
        "stateCountry": "CO",
        "city": "Trinidad",
        "postalCode": "81082",
        "county": "Las Animas",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.502510,
        "latitude": 37.168612,
        "googlePlaceId": None,
        "referenceId": "108",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "9b181fa5-a346-41e3-a70c-6fbf79b7b78a",
        "name": "Colorado Fingerprinting Kalamath (Open Mon-Sat)",
        "displayName": "PrintScan | Colorado Fingerprinting Kalamath (Open Mon-Sat) - Colorado Springs, CO",
        "description": "Suite 101",
        "metaDescription": "Welcome to PrintScan Denver, Colorado - your preferred choice for Live Scan and Fingerprinting services. Benefit from our fast, trustworthy, and secure solutions, specifically designed to cater to your unique requirements.",
        "notes": "Welcome to PrintScan Denver, Colorado - your preferred choice for Live Scan and Fingerprinting services. Benefit from our fast, trustworthy, and secure solutions, specifically designed to cater to your unique requirements.",
        "address1": "6547 N Academy Blvd",
        "address2": None,
        "stateCountry": "CO",
        "city": "Colorado Springs",
        "postalCode": "80918",
        "county": "Denver",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.792822,
        "latitude": 38.926942,
        "googlePlaceId": None,
        "referenceId": "43",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "06469851-7a3d-4ccd-87e6-6fc9a23085e8",
        "name": "Cloquet Mail Station Inc. - DBA Pack & Mail Room",
        "displayName": "Printscan Authorized Fingerprint Service Center - Duluth, MN",
        "description": None,
        "metaDescription": "Experience the best in Live Scan and Fingerprinting services with PrintScan in Duluth, Minnesota. Our advanced technology ensures accurate, dependable results. Trust PrintScan Duluth, Minnesota for all your fingerprinting needs.",
        "notes": "Experience the best in Live Scan and Fingerprinting services with PrintScan in Duluth, Minnesota. Our advanced technology ensures accurate, dependable results. Trust PrintScan Duluth, Minnesota for all your fingerprinting needs.",
        "address1": "1626 London Road",
        "address2": None,
        "stateCountry": "MN",
        "city": "Duluth",
        "postalCode": "55812",
        "county": "Saint Louis",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -92.075240,
        "latitude": 46.801149,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-06:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-06:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-06:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-06:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-06:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "175962b6-d7d6-4a60-8b91-713eb204c96f",
        "name": "Ankur PROD Location",
        "displayName": "PrintScan | Ankur PROD Location - Denver, CO",
        "description": "Ankur Sample Prod Description",
        "metaDescription": "Discover top-notch Live Scan and Fingerprinting services at PrintScan in Pueblo, Colorado. Our professional team is committed to providing efficient and reliable identification solutions. Choose PrintScan Pueblo for your security needs.",
        "notes": "Discover top-notch Live Scan and Fingerprinting services at PrintScan in Pueblo, Colorado. Our professional team is committed to providing efficient and reliable identification solutions. Choose PrintScan Pueblo for your security needs.",
        "address1": "700 14th St",
        "address2": None,
        "stateCountry": "CO",
        "city": "Denver",
        "postalCode": "80202",
        "county": "Pueblo",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.996572,
        "latitude": 39.742615,
        "googlePlaceId": None,
        "referenceId": "141",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "46247253-5dcd-4826-96e2-7170c7d1cb1e",
        "name": "Denver Metro Protective Services (Open Monday)",
        "displayName": "PrintScan | Denver Metro Protective Services (Open Monday) - Aurora, CO",
        "description": "Denver Metro Protective Services Suite 220",
        "metaDescription": "Visit PrintScan in Aurora, Colorado, your trusted destination for Live Scan and Fingerprinting services. Benefit from our swift, reliable, and personalized solutions designed to cater to your distinct needs.",
        "notes": "Visit PrintScan in Aurora, Colorado, your trusted destination for Live Scan and Fingerprinting services. Benefit from our swift, reliable, and personalized solutions designed to cater to your distinct needs.",
        "address1": "2121 S Blackhawk St Ste 230",
        "address2": None,
        "stateCountry": "CO",
        "city": "Aurora",
        "postalCode": "80014",
        "county": "Arapahoe",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.824402,
        "latitude": 39.677538,
        "googlePlaceId": None,
        "referenceId": "99",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "02d56903-2853-4332-a87d-72a1e3e4cec3",
        "name": "A and G Testing",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Tuscaloosa, AL",
        "description": None,
        "metaDescription": "Choose PrintScan in Tuscaloosa, Alabama for expert Live Scan and Fingerprinting services. We provide secure, efficient, and top-quality fingerprinting solutions to meet your specific needs.",
        "notes": "Choose PrintScan in Tuscaloosa, Alabama for expert Live Scan and Fingerprinting services. We provide secure, efficient, and top-quality fingerprinting solutions to meet your specific needs.",
        "address1": "2008 Paul W Bryant Drive",
        "address2": None,
        "stateCountry": "AL",
        "city": "Tuscaloosa",
        "postalCode": "35401",
        "county": "Tuscaloosa",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -87.561725,
        "latitude": 33.206637,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T12:00:00-06:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "62e54b2f-0f3d-44c0-8f89-72eb4a3c2c7b",
        "name": "Mainstreet Mailbox and Business Center LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Manteca, CA",
        "description": None,
        "metaDescription": "Explore PrintScan in Manteca, California, the leading provider of advanced Live Scan and Fingerprinting services. Benefit from our efficient, secure, and comprehensive identification solutions tailored to your needs.",
        "notes": "Explore PrintScan in Manteca, California, the leading provider of advanced Live Scan and Fingerprinting services. Benefit from our efficient, secure, and comprehensive identification solutions tailored to your needs.",
        "address1": "1231 N Mainstreet",
        "address2": None,
        "stateCountry": "CA",
        "city": "Manteca",
        "postalCode": "95336",
        "county": "San Joaquin",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -121.217768,
        "latitude": 37.814410,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-07:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-07:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-07:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-07:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-07:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T10:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-07:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "fff3bcbb-b32a-48be-b7a2-751e0a71bbe4",
        "name": "Loveland Police Department (Open Mon-Sat)",
        "displayName": "PrintScan | Loveland Police Department (Open Mon-Sat) - Loveland, CO",
        "description": "",
        "metaDescription": "Opt for PrintScan in Loveland, Colorado for reliable Live Scan and Fingerprinting services. We are committed to providing secure, efficient, and high-quality fingerprinting solutions tailored to your needs.",
        "notes": "Opt for PrintScan in Loveland, Colorado for reliable Live Scan and Fingerprinting services. We are committed to providing secure, efficient, and high-quality fingerprinting solutions tailored to your needs.",
        "address1": "810 E 10th St",
        "address2": None,
        "stateCountry": "CO",
        "city": "Loveland",
        "postalCode": "80537",
        "county": "Larimer",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -105.066523,
        "latitude": 40.400805,
        "googlePlaceId": None,
        "referenceId": "34",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "e5013bbf-7db1-4860-b7f3-76873e7eeac8",
        "name": "Testing Services - Chattanooga",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Chattanooga, TN",
        "description": None,
        "metaDescription": "Explore PrintScan in Chattanooga, Tennessee, your reliable choice for Live Scan and Fingerprinting services. Enjoy our speedy, trustworthy, and bespoke solutions designed to accommodate your specific requirements.",
        "notes": "Explore PrintScan in Chattanooga, Tennessee, your reliable choice for Live Scan and Fingerprinting services. Enjoy our speedy, trustworthy, and bespoke solutions designed to accommodate your specific requirements.",
        "address1": "5959 Shallowford Road, Suite 415",
        "address2": None,
        "stateCountry": "TN",
        "city": "Chattanooga",
        "postalCode": "37075",
        "county": None,
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -85.192643,
        "latitude": 35.055948,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:30:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "91d7616c-c63b-4543-a1da-789692124c17",
        "name": "TESTING SERVICES, LLC-LITTLE ROCK",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Little Rock, AR",
        "description": None,
        "metaDescription": "Visit PrintScan in Little Rock, Arkansas, your go-to source for superior Live Scan and Fingerprinting services. Enjoy our secure, fast, and reliable identification solutions designed to meet your specific requirements.",
        "notes": "Visit PrintScan in Little Rock, Arkansas, your go-to source for superior Live Scan and Fingerprinting services. Enjoy our secure, fast, and reliable identification solutions designed to meet your specific requirements.",
        "address1": "11908 Kanis Rd",
        "address2": "Suite G5",
        "stateCountry": "AR",
        "city": "Little Rock",
        "postalCode": "72211",
        "county": "Pulaski",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -92.406185,
        "latitude": 34.744588,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-06:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-06:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-06:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-06:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:30:00-06:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "26a0670f-7dd6-4149-9627-78aff1b494b8",
        "name": "Invicta (Open Thursday)",
        "displayName": "PrintScan | Invicta (Open Thursday) - Denver, CO",
        "description": "Navigate to \"Building 2\" which is the 2nd building on the left from the Turnpike Business Park entrance & access \"Unit 2-I\"",
        "metaDescription": "Get superior Live Scan and Fingerprinting services at PrintScan in Denver, Colorado. Our expert team delivers fast and reliable identification services. Rely on PrintScan Denver for all your identification and security requirements.",
        "notes": "Get superior Live Scan and Fingerprinting services at PrintScan in Denver, Colorado. Our expert team delivers fast and reliable identification services. Rely on PrintScan Denver for all your identification and security requirements.",
        "address1": "7100 Broadway",
        "address2": None,
        "stateCountry": "CO",
        "city": "Denver",
        "postalCode": "80221",
        "county": "Adams",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.986588,
        "latitude": 39.826490,
        "googlePlaceId": None,
        "referenceId": "106",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "031c8d8d-bda3-4c66-b2dd-78d7de2a120f",
        "name": "Partners for Youth (Open Tues-Wed)",
        "displayName": "PrintScan | Partners for Youth (Open Tues-Wed) - Steamboat Springs, CO",
        "description": "Unit 1",
        "metaDescription": "Choose PrintScan in Steamboat Springs, Colorado for exceptional Live Scan and Fingerprinting services. Our experienced team provides quick and trustworthy identification solutions. Count on PrintScan Steamboat Springs for your safety needs.",
        "notes": "Choose PrintScan in Steamboat Springs, Colorado for exceptional Live Scan and Fingerprinting services. Our experienced team provides quick and trustworthy identification solutions. Count on PrintScan Steamboat Springs for your safety needs.",
        "address1": "2673 Jacob Cir Unit #1",
        "address2": None,
        "stateCountry": "CO",
        "city": "Steamboat Springs",
        "postalCode": "80487",
        "county": "Routt",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -106.857624,
        "latitude": 40.507512,
        "googlePlaceId": None,
        "referenceId": "39",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "420fb001-30db-4604-8e31-794dd5831409",
        "name": "GW Defensive Driving",
        "displayName": "PrintScan Authorized Fingerprint Service Center- Macon, GA",
        "description": None,
        "metaDescription": "Visit PrintScan in Macon, Georgia, your premier choice for high-quality Live Scan and Fingerprinting services. Leverage our advanced technology for dependable and accurate results.",
        "notes": "Visit PrintScan in Macon, Georgia, your premier choice for high-quality Live Scan and Fingerprinting services. Leverage our advanced technology for dependable and accurate results.",
        "address1": "1375 Pio Nono Avenue",
        "address2": None,
        "stateCountry": "GA",
        "city": "Macon",
        "postalCode": "31204",
        "county": "Bibb",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -83.663204,
        "latitude": 32.832774,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "a0afae17-3697-41ff-9c3a-7dee7b54bf1f",
        "name": "Stat Diagnostics - Fredericksburg",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Fredericksburg, VA",
        "description": None,
        "metaDescription": "Experience unparalleled Live Scan and Fingerprinting services at PrintScan in Fredericksburg, Virginia. We pride ourselves on delivering fast, reliable, and precise identification solutions for all our clients.",
        "notes": "Experience unparalleled Live Scan and Fingerprinting services at PrintScan in Fredericksburg, Virginia. We pride ourselves on delivering fast, reliable, and precise identification solutions for all our clients.",
        "address1": "4528 Plank Road",
        "address2": "#103",
        "stateCountry": "VA",
        "city": "Fredericksburg",
        "postalCode": "22407",
        "county": "Culpeper",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -77.538430,
        "latitude": 38.286147,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T14:00:00-05:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T14:00:00-05:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T14:00:00-05:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T14:00:00-05:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T14:00:00-05:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "9a17c479-1bdf-4b01-8ef5-829c4b10b39a",
        "name": "Corner Gateway",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Slingerlands, NY",
        "description": None,
        "metaDescription": "Experience exceptional Live Scan and Fingerprinting services at PrintScan in Slingerlands, New York. Our skilled team offers quick and accurate results for all your identification tasks. Rely on PrintScan Slingerlands, NY for comprehensive and efficient fingerprinting needs.",
        "notes": "Experience exceptional Live Scan and Fingerprinting services at PrintScan in Slingerlands, New York. Our skilled team offers quick and accurate results for all your identification tasks. Rely on PrintScan Slingerlands, NY for comprehensive and efficient fingerprinting needs.",
        "address1": "1972 New Scotland Road",
        "address2": None,
        "stateCountry": "NY",
        "city": "Slingerlands",
        "postalCode": "12159",
        "county": "Albany",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -73.903063,
        "latitude": 42.631974,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "bfaa1aab-5a85-4faf-802d-83e1ce7a0e14",
        "name": "B&B Shipping (Open Tuesdays)",
        "displayName": "PrintScan | B&B Shipping (Open Tuesdays) - Leadville, CO",
        "description": "",
        "metaDescription": "Opt for PrintScan in Leadville, Colorado for high-quality Live Scan and Fingerprinting services. Our skilled team offers fast and dependable identification services. Trust in PrintScan Leadville for all your security and identification needs.",
        "notes": "Opt for PrintScan in Leadville, Colorado for high-quality Live Scan and Fingerprinting services. Our skilled team offers fast and dependable identification services. Trust in PrintScan Leadville for all your security and identification needs.",
        "address1": "518 Harrison Ave",
        "address2": None,
        "stateCountry": "CO",
        "city": "Leadville",
        "postalCode": "80461",
        "county": "Lake",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -106.291671,
        "latitude": 39.248735,
        "googlePlaceId": None,
        "referenceId": "132",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "7b7a0cad-9905-4967-a617-84189ea5e692",
        "name": "Wiley B&H Firearms LLC",
        "displayName": "Printscan Authorized Fingerprint Service Center - Fort Wayne, Indiana",
        "description": None,
        "metaDescription": "Get unparalleled Live Scan and Fingerprinting services at PrintScan in Fort Wayne, Indiana. Leveraging cutting-edge technology, we provide accurate and reliable results. Choose PrintScan Fort Wayne, Indiana for all your fingerprinting solutions.",
        "notes": "Get unparalleled Live Scan and Fingerprinting services at PrintScan in Fort Wayne, Indiana. Leveraging cutting-edge technology, we provide accurate and reliable results. Choose PrintScan Fort Wayne, Indiana for all your fingerprinting solutions.",
        "address1": "419 West Paulding Road",
        "address2": None,
        "stateCountry": "IN",
        "city": "Fort Wayne",
        "postalCode": "46807",
        "county": "Allen",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -85.141470,
        "latitude": 41.031394,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-05:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T10:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:30:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "8145715f-a457-49c9-88c4-86e99a75b09f",
        "name": "Erie Storage (Open Thursday)",
        "displayName": "PrintScan | Erie Storage (Open Thursday) - Erie, CO",
        "description": "Go to the main office",
        "metaDescription": "Trust PrintScan in Erie, Colorado for your Live Scan and Fingerprinting needs. We offer secure, efficient, and high-quality fingerprinting services, ensuring your complete satisfaction.",
        "notes": "Trust PrintScan in Erie, Colorado for your Live Scan and Fingerprinting needs. We offer secure, efficient, and high-quality fingerprinting services, ensuring your complete satisfaction.",
        "address1": "2831 Bonanza Dr",
        "address2": None,
        "stateCountry": "CO",
        "city": "Erie",
        "postalCode": "80516",
        "county": "Boulder",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -105.035331,
        "latitude": 40.002671,
        "googlePlaceId": None,
        "referenceId": "36",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "534104cb-87c2-46cf-8bb8-885e0c713deb",
        "name": "Douglas County DHS (Open Tues & Thurs)",
        "displayName": "PrintScan | Douglas County DHS (Open Tues & Thurs) - Castle Rock, CO",
        "description": "",
        "metaDescription": "Visit PrintScan in Castle Rock, Colorado for premium Live Scan and Fingerprinting services. Our proficient team is dedicated to providing swift and reliable identification solutions. Depend on PrintScan Castle Rock for your comprehensive security needs.",
        "notes": "Visit PrintScan in Castle Rock, Colorado for premium Live Scan and Fingerprinting services. Our proficient team is dedicated to providing swift and reliable identification solutions. Depend on PrintScan Castle Rock for your comprehensive security needs.",
        "address1": "4400 Castleton Ct",
        "address2": None,
        "stateCountry": "CO",
        "city": "Castle Rock",
        "postalCode": "80109",
        "county": "Douglas",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.865666,
        "latitude": 39.406459,
        "googlePlaceId": None,
        "referenceId": "76",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "ee6e8789-018a-4aac-aa81-8974989a39e2",
        "name": "Aims Community College Windsor (Open Thursday)",
        "displayName": "PrintScan | Aims Community College Windsor (Open Thursday) - Windsor, CO",
        "description": "Windsor Campus",
        "metaDescription": "Experience top-tier Live Scan and Fingerprinting services at PrintScan in Windsor, Colorado. Our professional team is committed to delivering quick and trustworthy identification services. Choose PrintScan Windsor for all your security and identification requirements.",
        "notes": "Experience top-tier Live Scan and Fingerprinting services at PrintScan in Windsor, Colorado. Our professional team is committed to delivering quick and trustworthy identification services. Choose PrintScan Windsor for all your security and identification requirements.",
        "address1": "1130 Southgate Dr",
        "address2": None,
        "stateCountry": "CO",
        "city": "Windsor",
        "postalCode": "80550",
        "county": "Larimer",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.915616,
        "latitude": 40.411957,
        "googlePlaceId": None,
        "referenceId": "94",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "1a8ca25e-02a7-4ee3-869b-8b096f91ea6f",
        "name": "Copy Plus Eagle (Open Tues-Fri)",
        "displayName": "PrintScan | Copy Plus Eagle (Open Tues-Fri) - Eagle, CO",
        "description": "",
        "metaDescription": "Choose PrintScan in Eagle, Colorado for unparalleled Live Scan and Fingerprinting services. Our dedicated team provides efficient and reliable identification solutions. Trust in PrintScan Eagle for all your safety and security needs.",
        "notes": "Choose PrintScan in Eagle, Colorado for unparalleled Live Scan and Fingerprinting services. Our dedicated team provides efficient and reliable identification solutions. Trust in PrintScan Eagle for all your safety and security needs.",
        "address1": "960 Chambers Ave",
        "address2": None,
        "stateCountry": "CO",
        "city": "Eagle",
        "postalCode": "81631",
        "county": "Eagle",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -106.815867,
        "latitude": 39.663727,
        "googlePlaceId": None,
        "referenceId": "49",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "c15e7751-3cf9-4943-98bb-8c64fc8e78e4",
        "name": "Robert Estelle LLC - The Exam Pros.",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Coconut Creek, FL",
        "description": None,
        "metaDescription": "Visit PrintScan in Coconut Creek, Florida, your trusted source for Live Scan and Fingerprinting services. Take advantage of our rapid, reliable, and personalized solutions crafted to address your unique requirements.",
        "notes": "Visit PrintScan in Coconut Creek, Florida, your trusted source for Live Scan and Fingerprinting services. Take advantage of our rapid, reliable, and personalized solutions crafted to address your unique requirements.",
        "address1": "4801 Johnson Rd",
        "address2": "Suite 13",
        "stateCountry": "FL",
        "city": "Coconut Creek",
        "postalCode": "33073",
        "county": "Broward",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.193347,
        "latitude": 26.312562,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "c52f4da6-a47a-4d64-87dc-928f9c20f938",
        "name": "Fastest Labs of Lakeland",
        "displayName": "PrintScan Authorized Fingerprint Service Center- Lakeland, FL",
        "description": None,
        "metaDescription": "Experience top-notch Live Scan and Fingerprinting services at PrintScan in Winter Garden, Florida. Utilize our innovative technology for trustworthy and precise outcomes every time.",
        "notes": "Experience top-notch Live Scan and Fingerprinting services at PrintScan in Winter Garden, Florida. Utilize our innovative technology for trustworthy and precise outcomes every time.",
        "address1": "1421 Commercial Park Dr",
        "address2": "Suite 4",
        "stateCountry": "FL",
        "city": "Lakeland",
        "postalCode": "33801",
        "county": "Polk",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.925560,
        "latitude": 28.025335,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "1d11c3db-bf27-4f93-9cf8-9396cf2f8cf0",
        "name": "JD & KD Warren Multi Service",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Washington, NJ",
        "description": None,
        "metaDescription": "Experience PrintScan in Washington, New Jersey, your go-to destination for Live Scan and Fingerprinting services. Leverage our efficient, trustworthy, and bespoke solutions designed to cater to your specific needs.",
        "notes": "Experience PrintScan in Washington, New Jersey, your go-to destination for Live Scan and Fingerprinting services. Leverage our efficient, trustworthy, and bespoke solutions designed to cater to your specific needs.",
        "address1": "412 E Washington Avenue",
        "address2": None,
        "stateCountry": "NJ",
        "city": "Washington",
        "postalCode": "07882",
        "county": "Warren",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -74.960651,
        "latitude": 40.763249,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:45:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:45:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:45:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:45:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:45:00-05:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:30:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "443c1bcf-67dc-4670-88e8-9492a47f65ed",
        "name": "True Scan Solutions LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Torrance, CA",
        "description": None,
        "metaDescription": "Explore PrintScan in Torrance, California, your reliable choice for Live Scan and Fingerprinting services. Enjoy our speedy, dependable, and customized solutions created to fulfill your distinct requirements.",
        "notes": "Explore PrintScan in Torrance, California, your reliable choice for Live Scan and Fingerprinting services. Enjoy our speedy, dependable, and customized solutions created to fulfill your distinct requirements.",
        "address1": "21151 S Western Avenue",
        "address2": "Suite 179",
        "stateCountry": "CA",
        "city": "Torrance",
        "postalCode": "90501",
        "county": "Los Angeles",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -118.309970,
        "latitude": 33.836964,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T11:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:30:00-07:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T11:00:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:30:00-07:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "28aba407-95d3-4c96-96c9-9529472676c6",
        "name": "First Choice Hire LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Charlotte, NC",
        "description": None,
        "metaDescription": "Choose PrintScan in Charlotte, North Carolina for efficient and secure Live Scan and Fingerprinting services. Our skilled team is dedicated to providing you with a seamless experience. Trust PrintScan Charlotte, North Carolina for all your identification solutions.",
        "notes": "Choose PrintScan in Charlotte, North Carolina for efficient and secure Live Scan and Fingerprinting services. Our skilled team is dedicated to providing you with a seamless experience. Trust PrintScan Charlotte, North Carolina for all your identification solutions.",
        "address1": "537 W Sugar Creek Road Suite 202",
        "address2": None,
        "stateCountry": "NC",
        "city": "Charlotte",
        "postalCode": "28213",
        "county": "Mecklenburg",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.795636,
        "latitude": 35.266365,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T12:00:00-05:00",
                "timeLunch": "2000-01-01T14:00:00-05:00",
                "timeResume": "2000-01-01T15:00:00-05:00",
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:30:00-05:00",
                "timeLunch": "2000-01-01T14:00:00-04:00",
                "timeResume": "2000-01-01T15:00:00-04:00",
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:30:00-05:00",
                "timeLunch": "2000-01-01T14:00:00-04:00",
                "timeResume": "2000-01-01T15:00:00-04:00",
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:30:00-05:00",
                "timeLunch": "2000-01-01T14:00:00-04:00",
                "timeResume": "2000-01-01T15:00:00-04:00",
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:30:00-05:00",
                "timeLunch": "2000-01-01T14:00:00-04:00",
                "timeResume": "2000-01-01T15:00:00-04:00",
                "timeClose": "2000-01-01T18:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "99b5cab9-cbcd-44bc-9f8f-9651f3472554",
        "name": "ARCPoint Labs of Bellingham",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Bellingham, WA",
        "description": None,
        "metaDescription": "Explore PrintScan Bellingham, Washington - your trusted hub for Live Scan and Fingerprinting services. Take advantage of our quick, dependable, and confidential solutions, tailored to meet your specific requirements.",
        "notes": "Explore PrintScan Bellingham, Washington - your trusted hub for Live Scan and Fingerprinting services. Take advantage of our quick, dependable, and confidential solutions, tailored to meet your specific requirements.",
        "address1": "4220 Meridian Street ",
        "address2": "Suite 101A",
        "stateCountry": "WA",
        "city": "Bellingham",
        "postalCode": "98226",
        "county": "Whatcom",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -122.485373,
        "latitude": 48.794446,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "f8e75130-f53c-4cf4-b183-97e2ef463ed7",
        "name": "Giving Dream - NYC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- NYC, 32nd St",
        "description": None,
        "metaDescription": "Experience top-notch Live Scan and Fingerprinting services at PrintScan in New York, New York. We offer secure, efficient, and reliable identification solutions to meet your unique needs.",
        "notes": "Experience top-notch Live Scan and Fingerprinting services at PrintScan in New York, New York. We offer secure, efficient, and reliable identification solutions to meet your unique needs.",
        "address1": "38 West 32nd Street",
        "address2": "Suite 1507",
        "stateCountry": "NY",
        "city": "New York",
        "postalCode": "10001-3816",
        "county": "New York",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -73.987404,
        "latitude": 40.747781,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": "2000-01-01T13:00:00-04:00",
                "timeResume": "2000-01-01T14:00:00-04:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": "2000-01-01T13:00:00-04:00",
                "timeResume": "2000-01-01T14:00:00-04:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": "2000-01-01T13:00:00-04:00",
                "timeResume": "2000-01-01T14:00:00-04:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": "2000-01-01T13:00:00-04:00",
                "timeResume": "2000-01-01T14:00:00-04:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": "2000-01-01T13:00:00-04:00",
                "timeResume": "2000-01-01T14:00:00-04:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b191213c-b97e-498d-8c28-9b912acae818",
        "name": "Amani Grace Diagnostics",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Owosso, MI",
        "description": None,
        "metaDescription": "Experience fast and accurate Live Scan and Fingerprinting services in Owosso, Michigan with PrintScan - a trusted name in security solutions. Secure your peace of mind today with our state-of-the-art technology.",
        "notes": "Experience fast and accurate Live Scan and Fingerprinting services in Owosso, Michigan with PrintScan - a trusted name in security solutions. Secure your peace of mind today with our state-of-the-art technology.",
        "address1": "810 W Main Street",
        "address2": None,
        "stateCountry": "MI",
        "city": "Owosso",
        "postalCode": "48867",
        "county": "Shiawassee",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -84.182284,
        "latitude": 42.997784,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:30:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "7a9caa15-5f66-40cd-8606-9c179c760e4d",
        "name": "Prairie Family Center Burlington (Open Tues-Thurs)",
        "displayName": "PrintScan | Prairie Family Center Burlington (Open Tues-Thurs) - Burlington, CO",
        "description": "",
        "metaDescription": "Opt for PrintScan in Burlington, Colorado for superior Live Scan and Fingerprinting services. Our skilled team is dedicated to providing swift and reliable identification services. Trust PrintScan Burlington for all your security and identification requirements.",
        "notes": "Opt for PrintScan in Burlington, Colorado for superior Live Scan and Fingerprinting services. Our skilled team is dedicated to providing swift and reliable identification services. Trust PrintScan Burlington for all your security and identification requirements.",
        "address1": "1040 Rose Ave",
        "address2": None,
        "stateCountry": "CO",
        "city": "Burlington",
        "postalCode": "80807",
        "county": "Kit Carson",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -102.263252,
        "latitude": 39.301570,
        "googlePlaceId": None,
        "referenceId": "6",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "2283fae8-95ce-40d0-8be4-9caac0744a2f",
        "name": "Pagosa Photography (Open Mon-Fri)",
        "displayName": "PrintScan | Pagosa Photography (Open Mon-Fri) - Pagosa Springs, CO",
        "description": "",
        "metaDescription": "Experience top-notch Live Scan and Fingerprinting services at PrintScan in Pagosa Springs, Colorado. Our professional team delivers quick and trustworthy identification solutions. Choose PrintScan Pagosa Springs for your comprehensive security needs.",
        "notes": "Experience top-notch Live Scan and Fingerprinting services at PrintScan in Pagosa Springs, Colorado. Our professional team delivers quick and trustworthy identification solutions. Choose PrintScan Pagosa Springs for your comprehensive security needs.",
        "address1": "480 San Juan St",
        "address2": None,
        "stateCountry": "CO",
        "city": "Pagosa Springs",
        "postalCode": "81147",
        "county": "Archuleta",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -107.011771,
        "latitude": 37.266464,
        "googlePlaceId": None,
        "referenceId": "80",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "51691452-04e2-4d5a-8cbe-9ce36a581e88",
        "name": "Colorado Mobile Drug Testing Fort Morgan (Open Mon-Fri)",
        "displayName": "PrintScan | Colorado Mobile Drug Testing Fort Morgan (Open Mon-Fri) - Fort Morgan, CO",
        "description": "",
        "metaDescription": "Choose PrintScan in Fort Morgan, Colorado for exceptional Live Scan and Fingerprinting services. We offer secure, efficient, and high-quality fingerprinting solutions tailored to your specific needs.",
        "notes": "Choose PrintScan in Fort Morgan, Colorado for exceptional Live Scan and Fingerprinting services. We offer secure, efficient, and high-quality fingerprinting solutions tailored to your specific needs.",
        "address1": "411 W Platte Ave unit b",
        "address2": None,
        "stateCountry": "CO",
        "city": "Fort Morgan",
        "postalCode": "80701",
        "county": "Morgan",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -103.806943,
        "latitude": 40.254345,
        "googlePlaceId": None,
        "referenceId": "21",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "20cf636a-0b7a-ec11-94f6-a04a5e9ba6a6",
        "name": "VREITZ Fingerprints & Background Check Prep",
        "displayName": "PrintScan - Authorized Fingerprint Service Center",
        "description": None,
        "metaDescription": "Find exceptional Live Scan and Fingerprinting services at PrintScan in Salt Lake City, Utah. Our innovative technology ensures rapid and accurate results, catering to all your identification requirements. Depend on PrintScan Salt Lake City, UT for secure and efficient fingerprinting solutions.",
        "notes": "Find exceptional Live Scan and Fingerprinting services at PrintScan in Salt Lake City, Utah. Our innovative technology ensures rapid and accurate results, catering to all your identification requirements. Depend on PrintScan Salt Lake City, UT for secure and efficient fingerprinting solutions.",
        "address1": "2828 W 4700",
        "address2": "Unit D",
        "stateCountry": "UT",
        "city": "Taylorsville",
        "postalCode": "84129",
        "county": "Salt Lake",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -111.960504,
        "latitude": 40.667885,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2022-12-08T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-12-08T19:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2022-12-08T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-12-08T19:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2022-12-08T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-12-08T19:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2022-12-08T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-12-08T19:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2022-12-08T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-12-08T19:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T12:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "c902d0cb-f57d-ec11-94f6-a04a5e9ba6a6",
        "name": "Fingerprinting Pros Inc",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Las Vegas, NV",
        "description": "Corner of Maryland and Sahara in Smiths Shopping Center",
        "metaDescription": "Welcome to PrintScan in Las Vegas, Nevada, your go-to hub for top-notch Live Scan and Fingerprinting services. Enjoy our swift, secure, and trusted fingerprinting processes at PrintScan Las Vegas today.",
        "notes": "Welcome to PrintScan in Las Vegas, Nevada, your go-to hub for top-notch Live Scan and Fingerprinting services. Enjoy our swift, secure, and trusted fingerprinting processes at PrintScan Las Vegas today.",
        "address1": "2620 S Maryland Pkwy",
        "address2": "Suite 17",
        "stateCountry": "NV",
        "city": "Las Vegas",
        "postalCode": "89109",
        "county": "Clark",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -115.135259,
        "latitude": 36.141908,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:15:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:15:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:15:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:15:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:15:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "d068f90e-127e-ec11-94f6-a04a5e9ba6a6",
        "name": "Spyder Arms",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Alexandria, KY",
        "description": None,
        "metaDescription": "Experience superior Live Scan and Fingerprinting services at PrintScan in Alexandria, Kentucky. Our expert team is committed to delivering fast and accurate results for all your identification needs. Trust in PrintScan Alexandria for your secure and reliable identification solutions.",
        "notes": "Experience superior Live Scan and Fingerprinting services at PrintScan in Alexandria, Kentucky. Our expert team is committed to delivering fast and accurate results for all your identification needs. Trust in PrintScan Alexandria for your secure and reliable identification solutions.",
        "address1": "7907 Alexandria Pike",
        "address2": None,
        "stateCountry": "KY",
        "city": "Alexandria",
        "postalCode": "41001",
        "county": "Campbell",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -84.393252,
        "latitude": 38.969424,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "9d6df0c3-7083-ec11-94f6-a04a5e9ba6a6",
        "name": "West Armory",
        "displayName": "PrintScan - Authorized Fingerprint Service Center",
        "description": None,
        "metaDescription": "Experience exceptional Live Scan and Fingerprinting services at PrintScan in Dade City, Florida. Our dedicated team ensures quick, reliable, and personalized services. Rely on PrintScan Dade City, FL for all your fingerprinting and live scan requirements.",
        "notes": "Experience exceptional Live Scan and Fingerprinting services at PrintScan in Dade City, Florida. Our dedicated team ensures quick, reliable, and personalized services. Rely on PrintScan Dade City, FL for all your fingerprinting and live scan requirements.",
        "address1": "15029 US-301",
        "address2": None,
        "stateCountry": "FL",
        "city": "Dade City",
        "postalCode": "33523",
        "county": "Pasco",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -82.192500,
        "latitude": 28.376667,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "42cd158f-0c64-ec11-94f6-a04a5e9ba6a8",
        "name": "Secure Imprint",
        "displayName": "PrintScan - Authorized Fingerprint Service Center",
        "description": "Building 400 inside Airport Office Centre Plaza. Building has about 3 different entrances.",
        "metaDescription": "Discover PrintScan in Indianapolis, Indiana, your reliable choice for comprehensive Live Scan and Fingerprinting services. Take advantage of our quick, accurate, and dependable solutions now!",
        "notes": "Discover PrintScan in Indianapolis, Indiana, your reliable choice for comprehensive Live Scan and Fingerprinting services. Take advantage of our quick, accurate, and dependable solutions now!",
        "address1": "2346 S. Lynhurst Drive",
        "address2": "Suite 407K",
        "stateCountry": "IN",
        "city": "Indianapolis",
        "postalCode": "46241",
        "county": "Marion",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -86.251928,
        "latitude": 39.732500,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00+00:00",
                "timeResume": "2000-01-01T13:00:00+00:00",
                "timeClose": "2000-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00+00:00",
                "timeResume": "2000-01-01T13:00:00+00:00",
                "timeClose": "2000-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00+00:00",
                "timeResume": "2000-01-01T13:00:00+00:00",
                "timeClose": "2000-01-01T19:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00+00:00",
                "timeResume": "2000-01-01T13:00:00+00:00",
                "timeClose": "2000-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": "2000-01-01T12:00:00+00:00",
                "timeResume": "2000-01-01T13:00:00+00:00",
                "timeClose": "2000-01-01T16:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "da76ea06-2464-ec11-94f6-a04a5e9ba6a8",
        "name": "Axiom Premier Signing Services",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Orange Park, FL",
        "description": None,
        "metaDescription": "Turn to PrintScan in Orange Park, Florida for high-quality Live Scan and Fingerprinting services. We are committed to providing fast, secure, and precise identification solutions to meet your unique needs.",
        "notes": "Turn to PrintScan in Orange Park, Florida for high-quality Live Scan and Fingerprinting services. We are committed to providing fast, secure, and precise identification solutions to meet your unique needs.",
        "address1": "794 Foxridge Center Dr",
        "address2": "Suite 101",
        "stateCountry": "FL",
        "city": "Orange Park",
        "postalCode": "32065",
        "county": "Clay",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.764453,
        "latitude": 30.144968,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "055e48ea-2764-ec11-94f6-a04a5e9ba6a8",
        "name": "1602 Solutions Agency",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Nashville, TN",
        "description": "Directly Across the Street from Mr. Car Wash",
        "metaDescription": "Choose PrintScan in Nashville, Tennessee for premier Live Scan and Fingerprinting services. We provide high-quality, reliable identification solutions tailored to your specific needs.",
        "notes": "Choose PrintScan in Nashville, Tennessee for premier Live Scan and Fingerprinting services. We provide high-quality, reliable identification solutions tailored to your specific needs.",
        "address1": "2131 Murfreesboro Pike",
        "address2": "Suite 204D",
        "stateCountry": "TN",
        "city": "Nashville",
        "postalCode": "37217",
        "county": "Davidson",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -86.652500,
        "latitude": 36.092339,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2022-09-21T09:00:00+00:00",
                "timeLunch": "2022-09-21T13:30:00+00:00",
                "timeResume": "2022-09-21T15:00:00+00:00",
                "timeClose": "2022-09-21T18:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2022-09-21T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T13:30:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-07-28T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T13:30:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-07-28T09:00:00+00:00",
                "timeLunch": "2000-01-01T13:30:00-05:00",
                "timeResume": "2000-01-01T15:00:00-05:00",
                "timeClose": "2023-07-28T18:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-07-28T09:00:00+00:00",
                "timeLunch": "2000-01-01T13:30:00-05:00",
                "timeResume": "2000-01-01T15:00:00-05:00",
                "timeClose": "2023-07-28T18:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "1ad0c94b-c670-ec11-94f6-a04a5e9ba6a8",
        "name": "NTO Financial",
        "displayName": "PrintScan - Authorized Fingerprint Service Center",
        "description": None,
        "metaDescription": "Experience exceptional Live Scan and Fingerprinting services at PrintScan in Joliet, Illinois. Our dedicated professionals provide swift and precise results, making us your preferred choice for all your identification needs. Trust PrintScan Joliet for reliable and efficient fingerprinting solutions.",
        "notes": "Experience exceptional Live Scan and Fingerprinting services at PrintScan in Joliet, Illinois. Our dedicated professionals provide swift and precise results, making us your preferred choice for all your identification needs. Trust PrintScan Joliet for reliable and efficient fingerprinting solutions.",
        "address1": "1000 Essington Road",
        "address2": None,
        "stateCountry": "IL",
        "city": "Joliet",
        "postalCode": "60435",
        "county": "Will",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -88.159861,
        "latitude": 41.539783,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-01T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-01T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-01T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-01T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-01T08:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-01T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "8a38bfcb-f193-ec11-a507-a04a5e9bb069",
        "name": "BioScan Tek",
        "displayName": "PrintScan - Authorized Fingerprint Service Center",
        "description": "Go to building C and enter the 1700 door (Big white letters 1700 with call box), go past elevator, make immediate left, through glass door then down the hall to BioScan Tek unit 1615.",
        "metaDescription": "Explore high-quality Live Scan and Fingerprinting services at PrintScan in Wheaton, Illinois. Our expert team guarantees precise results for all your identification processes. Choose PrintScan Wheaton for your dependable security solutions.",
        "notes": "Explore high-quality Live Scan and Fingerprinting services at PrintScan in Wheaton, Illinois. Our expert team guarantees precise results for all your identification processes. Choose PrintScan Wheaton for your dependable security solutions.",
        "address1": "2100 Manchester Rd",
        "address2": "Building C- #1615",
        "stateCountry": "IL",
        "city": "Wheaton",
        "postalCode": "60187",
        "county": "Dupage",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -88.138251,
        "latitude": 41.864711,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-04-11T10:00:00+00:00",
                "timeLunch": "2023-04-11T12:30:00+00:00",
                "timeResume": "2023-04-11T13:30:00+00:00",
                "timeClose": "2023-04-11T17:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-04-11T10:00:00+00:00",
                "timeLunch": "2023-04-11T12:30:00+00:00",
                "timeResume": "2023-04-11T13:30:00+00:00",
                "timeClose": "2023-04-11T17:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-04-11T10:00:00+00:00",
                "timeLunch": "2023-04-11T12:30:00+00:00",
                "timeResume": "2023-04-11T13:30:00+00:00",
                "timeClose": "2023-04-11T17:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-04-11T10:00:00+00:00",
                "timeLunch": "2023-04-11T12:30:00+00:00",
                "timeResume": "2023-04-11T13:30:00+00:00",
                "timeClose": "2023-04-11T17:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "414f3d9b-2414-ed11-bd6e-a04a5e9bb069",
        "name": "The Notary Seal Fingerprinting(Fredericksburg)",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Fredericksburg, VA",
        "description": "Westwood Office Park Building Complex \"The Notary Seal Fingerprinting\"-540.410.2929",
        "metaDescription": "Experience unparalleled Live Scan and Fingerprinting services at PrintScan in Fredericksburg, Virginia. We pride ourselves on delivering fast, reliable, and precise identification solutions for all our clients.",
        "notes": "Experience unparalleled Live Scan and Fingerprinting services at PrintScan in Fredericksburg, Virginia. We pride ourselves on delivering fast, reliable, and precise identification solutions for all our clients.",
        "address1": "405 Westwood Office Park",
        "address2": None,
        "stateCountry": "VA",
        "city": "Fredericksburg",
        "postalCode": "22401",
        "county": "Fredericksburg City",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -77.494603,
        "latitude": 38.296766,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-14T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:45:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-14T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:45:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-14T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:45:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-14T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:45:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-14T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:45:00-04:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-08-14T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-14T12:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "d88027c6-ef17-ed11-bd6e-a04a5e9bb069",
        "name": "Horta's and Associates Group",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Miami, FL",
        "description": None,
        "metaDescription": "Explore PrintScan in Miami, Florida, your premier choice for advanced Live Scan and Fingerprinting services. Benefit from our swift, secure, and dependable fingerprinting processes at PrintScan Miami today.",
        "notes": "Explore PrintScan in Miami, Florida, your premier choice for advanced Live Scan and Fingerprinting services. Benefit from our swift, secure, and dependable fingerprinting processes at PrintScan Miami today.",
        "address1": "8242 W Flagler St",
        "address2": None,
        "stateCountry": "FL",
        "city": "Miami",
        "postalCode": "33144",
        "county": "Miami-Dade",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.329166,
        "latitude": 25.769392,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "ae9e75ca-f117-ed11-bd6e-a04a5e9bb069",
        "name": "CRC Onboarding Services - Charlotte, NC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Charlotte, NC",
        "description": "Fingerprints by Appointment Only please - Office is located at 2133 S. Blvd, for GPS purposes please use 107 Southend Drive (Suite 107) to bring you closer to the front door.",
        "metaDescription": "Choose PrintScan in Charlotte, North Carolina for efficient and secure Live Scan and Fingerprinting services. Our skilled team is dedicated to providing you with a seamless experience. Trust PrintScan Charlotte, North Carolina for all your identification solutions.",
        "notes": "Choose PrintScan in Charlotte, North Carolina for efficient and secure Live Scan and Fingerprinting services. Our skilled team is dedicated to providing you with a seamless experience. Trust PrintScan Charlotte, North Carolina for all your identification solutions.",
        "address1": "2133 S Blvd",
        "address2": None,
        "stateCountry": "NC",
        "city": "Charlotte",
        "postalCode": "28203",
        "county": "Mecklenburg",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.860047,
        "latitude": 35.207139,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": "2000-01-01T12:00:00-05:00",
                "timeResume": "2000-01-01T13:00:00-05:00",
                "timeClose": "2000-01-01T16:45:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": "2000-01-01T12:00:00-05:00",
                "timeResume": "2000-01-01T13:00:00-05:00",
                "timeClose": "2000-01-01T16:45:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": "2000-01-01T12:00:00-05:00",
                "timeResume": "2000-01-01T13:00:00-05:00",
                "timeClose": "2000-01-01T16:45:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": "2000-01-01T12:00:00-05:00",
                "timeResume": "2000-01-01T13:00:00-05:00",
                "timeClose": "2000-01-01T16:45:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00-04:00",
                "timeLunch": "2000-01-01T12:00:00-05:00",
                "timeResume": "2000-01-01T13:00:00-05:00",
                "timeClose": "2000-01-01T16:45:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "9db26176-681d-ed11-bd6e-a04a5e9bb069",
        "name": "BET Professional Service Inc.",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Lauderhill, FL",
        "description": "Across Wawa gas station, 44th st",
        "metaDescription": "Visit PrintScan in Lauderhill, Florida for superior Live Scan and Fingerprinting services. Our dedicated team offers quick and precise identification solutions. Rely on PrintScan Lauderhill for all your professional fingerprinting needs.",
        "notes": "Visit PrintScan in Lauderhill, Florida for superior Live Scan and Fingerprinting services. Our dedicated team offers quick and precise identification solutions. Rely on PrintScan Lauderhill for all your professional fingerprinting needs.",
        "address1": "4300 N University Drive",
        "address2": "Suite E-206",
        "stateCountry": "FL",
        "city": "Lauderhill",
        "postalCode": "33351",
        "county": "Broward",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.250558,
        "latitude": 26.178323,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "d4fd0010-f81f-ed11-bd6e-a04a5e9bb069",
        "name": "10-8.Blue LLC",
        "displayName": "10-8.Blue LLC",
        "description": None,
        "metaDescription": "Choose PrintScan in Las Cruces, New Mexico for superior Live Scan and Fingerprinting services. We offer state-of-the-art identification solutions for your security needs.",
        "notes": "Choose PrintScan in Las Cruces, New Mexico for superior Live Scan and Fingerprinting services. We offer state-of-the-art identification solutions for your security needs.",
        "address1": "2001 E Lohman Ave",
        "address2": "Ste 110-145",
        "stateCountry": "NM",
        "city": "Las Cruces",
        "postalCode": "88001",
        "county": "Dona Ana",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -106.757052,
        "latitude": 32.311436,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2020-01-01T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "5b8d27a1-a974-ec11-94f6-a04a5e9bb06a",
        "name": "CR Sales Firearms",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Jackson, MO",
        "description": None,
        "metaDescription": "Discover top-notch Live Scan and Fingerprinting services at PrintScan in Independence, Missouri. We provide precise and efficient solutions for all your identification requirements. Stop by our location today!",
        "notes": "Discover top-notch Live Scan and Fingerprinting services at PrintScan in Independence, Missouri. We provide precise and efficient solutions for all your identification requirements. Stop by our location today!",
        "address1": "1703 S Noland Rd",
        "address2": None,
        "stateCountry": "MO",
        "city": "Independence",
        "postalCode": "64055",
        "county": "Jackson",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -94.413764,
        "latitude": 39.071507,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "f4f50df9-6875-ec11-94f6-a04a5e9bb06a",
        "name": "Cora LLC: DBA FIngerprints Plus",
        "displayName": "PrintScan Authorized Fingerprint Service Center- Sterling, VA",
        "description": "Suite 120B is part of Suite 120. Located in same hallway/entrance as Virginia Gold Buyers.",
        "metaDescription": "Get high-quality Live Scan and Fingerprinting services at PrintScan in Sterling, Virginia. Our professional team delivers accurate and prompt results for all your identification needs. Visit us today for exceptional service!",
        "notes": "Get high-quality Live Scan and Fingerprinting services at PrintScan in Sterling, Virginia. Our professional team delivers accurate and prompt results for all your identification needs. Visit us today for exceptional service!",
        "address1": "21580 Atlantic Blvd",
        "address2": "Suite 120B",
        "stateCountry": "VA",
        "city": "Sterling",
        "postalCode": "20166",
        "county": "Loudoun",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -77.423042,
        "latitude": 39.019284,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "048fd49c-b89f-ec11-a22a-a04a5e9bb06a",
        "name": "Aloha Fingerprints",
        "displayName": "PrintScan - Authorized Fingerprint Service Center",
        "description": None,
        "metaDescription": "Experience the best in Live Scan and Fingerprinting services at PrintScan in Litchfield Park, Arizona. Our skilled team is committed to delivering fast and accurate identification services. Trust in PrintScan Litchfield Park for all your identification needs.",
        "notes": "Experience the best in Live Scan and Fingerprinting services at PrintScan in Litchfield Park, Arizona. Our skilled team is committed to delivering fast and accurate identification services. Trust in PrintScan Litchfield Park for all your identification needs.",
        "address1": "501 E. Plaza Circle",
        "address2": "Suite 15",
        "stateCountry": "AZ",
        "city": "Litchfield Park",
        "postalCode": "85340",
        "county": "Maricopa",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -112.350142,
        "latitude": 33.487315,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-04-11T08:30:00+00:00",
                "timeLunch": "2023-04-11T12:00:00+00:00",
                "timeResume": "2023-04-11T13:00:00+00:00",
                "timeClose": "2023-04-11T18:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-04-11T08:30:00+00:00",
                "timeLunch": "2023-04-11T12:00:00+00:00",
                "timeResume": "2023-04-11T13:00:00+00:00",
                "timeClose": "2023-04-11T18:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-09-21T08:30:00+00:00",
                "timeLunch": "2023-09-21T12:00:00+00:00",
                "timeResume": "2023-09-21T13:00:00+00:00",
                "timeClose": "2023-09-21T18:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-04-11T08:30:00+00:00",
                "timeLunch": "2023-04-11T12:00:00+00:00",
                "timeResume": "2023-04-11T13:00:00+00:00",
                "timeClose": "2023-04-11T18:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-04-11T08:30:00+00:00",
                "timeLunch": "2023-04-11T12:00:00+00:00",
                "timeResume": "2023-04-11T13:00:00+00:00",
                "timeClose": "2023-04-11T18:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "9d0e0833-74a4-ec11-a22a-a04a5e9bb06a",
        "name": "Elite Shooting Range",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Murrells Inlet, SC",
        "description": "Located inside Elite Shooting Range",
        "metaDescription": "Visit PrintScan in Murrells Inlet, South Carolina for top-tier Live Scan and Fingerprinting services. Our dedicated team provides swift and accurate identification solutions. Choose PrintScan Murrells Inlet for trusted and reliable results in all your identification needs.",
        "notes": "Visit PrintScan in Murrells Inlet, South Carolina for top-tier Live Scan and Fingerprinting services. Our dedicated team provides swift and accurate identification solutions. Choose PrintScan Murrells Inlet for trusted and reliable results in all your identification needs.",
        "address1": "3418 US-17 BUS",
        "address2": None,
        "stateCountry": "SC",
        "city": "Murrells Inlet",
        "postalCode": "29576",
        "county": "Horry",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -79.026104,
        "latitude": 33.574625,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b06e5b2e-6c4c-ec11-9820-a04a5e9bba27",
        "name": "Heart's Desire Background Screening",
        "displayName": "PrintScan Authorized Fingerprint Service Center - St Petersburg, FL",
        "description": "Tap the “Virtual Key” button on the intercom, then use one of the options: PIN code: Enter the 6-digit PIN code provided and press “enter” to open the door/gate (PIN Code: 702934)",
        "metaDescription": "Choose PrintScan in St. Petersburg, Florida for exceptional Live Scan and Fingerprinting services. Our team is dedicated to providing quick and accurate identification solutions. Trust PrintScan St. Petersburg, FL for all your secure fingerprinting requirements.",
        "notes": "Choose PrintScan in St. Petersburg, Florida for exceptional Live Scan and Fingerprinting services. Our team is dedicated to providing quick and accurate identification solutions. Trust PrintScan St. Petersburg, FL for all your secure fingerprinting requirements.",
        "address1": "333 3rd Avenue N",
        "address2": "Suite 200B",
        "stateCountry": "FL",
        "city": "St. Petersburg",
        "postalCode": "33701",
        "county": "Pinellas",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -82.638173,
        "latitude": 27.775166,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "7b23e6f3-218d-47f5-9bf8-a0b01f736922",
        "name": "Hilltop Family Resource Center (Open Tues & Thurs)",
        "displayName": "PrintScan | Hilltop Family Resource Center (Open Tues & Thurs) - Grand Junction, CO",
        "description": "",
        "metaDescription": "Visit PrintScan in Grand Junction, Colorado for high-quality Live Scan and Fingerprinting services. Our proficient team is committed to providing efficient and reliable identification services. Depend on PrintScan Grand Junction for all your safety and security requirements.",
        "notes": "Visit PrintScan in Grand Junction, Colorado for high-quality Live Scan and Fingerprinting services. Our proficient team is committed to providing efficient and reliable identification services. Depend on PrintScan Grand Junction for all your safety and security requirements.",
        "address1": "1129 Colorado Ave",
        "address2": None,
        "stateCountry": "CO",
        "city": "Grand Junction",
        "postalCode": "81501",
        "county": "Mesa",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -108.553546,
        "latitude": 39.066118,
        "googlePlaceId": None,
        "referenceId": "24",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "4081dc97-c23d-4a6f-b6f7-a147e0f1b960",
        "name": "Copy Copy Glenwood Springs (Open Tu-Fri)",
        "displayName": "PrintScan | Copy Copy Glenwood Springs (Open Tu-Fri) - Glenwood Springs, CO",
        "description": "",
        "metaDescription": "Choose PrintScan in Glenwood Springs, Colorado for premium Live Scan and Fingerprinting services. Our expert team offers fast and dependable identification solutions. Trust in PrintScan Glenwood Springs for all your identification and security needs.",
        "notes": "Choose PrintScan in Glenwood Springs, Colorado for premium Live Scan and Fingerprinting services. Our expert team offers fast and dependable identification solutions. Trust in PrintScan Glenwood Springs for all your identification and security needs.",
        "address1": "2826 B",
        "address2": None,
        "stateCountry": "CO",
        "city": "Glenwood Springs",
        "postalCode": "81601",
        "county": "Garfield",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -107.321582,
        "latitude": 39.523832,
        "googlePlaceId": None,
        "referenceId": "23",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b27217c8-32dd-4a35-b65b-a83b356c8a97",
        "name": "Prime Development Alliance LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Troy, MI",
        "description": "Come through parking lot entrance in back. First door on right facing building.",
        "metaDescription": "Choose PrintScan in Troy, Michigan for superior Live Scan and Fingerprinting services. We provide secure, efficient, and professional identification solutions tailored to your specific needs.",
        "notes": "Choose PrintScan in Troy, Michigan for superior Live Scan and Fingerprinting services. We provide secure, efficient, and professional identification solutions tailored to your specific needs.",
        "address1": "2328 Livernois Road",
        "address2": "Suite 1010",
        "stateCountry": "MI",
        "city": "Troy",
        "postalCode": "48083",
        "county": "Oakland",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -83.146945,
        "latitude": 42.556442,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:30:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:30:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:30:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:30:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:30:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "de2f72a4-0552-4cc2-bde0-ac4ebd424d1c",
        "name": "APITesting",
        "displayName": "PrintScan | APITesting - Westchester, IL",
        "description": "APITesting",
        "metaDescription": "Explore PrintScan in Monument, Colorado, your reliable source for advanced Live Scan and Fingerprinting services. Enjoy precise, quick, and safe options for all your personal identification requirements.",
        "notes": "Explore PrintScan in Monument, Colorado, your reliable source for advanced Live Scan and Fingerprinting services. Enjoy precise, quick, and safe options for all your personal identification requirements.",
        "address1": "60154",
        "address2": None,
        "stateCountry": "IL",
        "city": "Westchester",
        "postalCode": "60154",
        "county": "El Paso",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -87.889338,
        "latitude": 41.845718,
        "googlePlaceId": None,
        "referenceId": "146",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "35e5bb24-fa50-456d-8c11-b1877f4cf3c1",
        "name": "YMCA Estes Park (Open Wednesdays)",
        "displayName": "PrintScan | YMCA Estes Park (Open Wednesdays) - Estes Park, CO",
        "description": "Check in at the Administration Building with Human Resources",
        "metaDescription": "Experience top-tier Live Scan and Fingerprinting services at PrintScan in Estes Park, Colorado. Our professional team delivers quick and trustworthy identification solutions. Choose PrintScan Estes Park for your comprehensive security needs.",
        "notes": "Experience top-tier Live Scan and Fingerprinting services at PrintScan in Estes Park, Colorado. Our professional team delivers quick and trustworthy identification solutions. Choose PrintScan Estes Park for your comprehensive security needs.",
        "address1": "2515 Tunnel Rd",
        "address2": None,
        "stateCountry": "CO",
        "city": "Estes Park",
        "postalCode": "80511",
        "county": "Larimer",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -105.566154,
        "latitude": 40.340370,
        "googlePlaceId": None,
        "referenceId": "95",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "71594949-8e81-417a-9cf0-b3184e1a332e",
        "name": "Colorado Fingerprinting Smoky Hill Library (Open Mon & Fri)",
        "displayName": "PrintScan | Colorado Fingerprinting Smoky Hill Library (Open Mon & Fri) - Centennial, CO",
        "description": "Smoky Hill Library",
        "metaDescription": "Discover PrintScan in Centennial, Colorado, your premier provider for Live Scan and Fingerprinting services. Benefit from our swift, secure, and tailored solutions designed to meet your unique needs.",
        "notes": "Discover PrintScan in Centennial, Colorado, your premier provider for Live Scan and Fingerprinting services. Benefit from our swift, secure, and tailored solutions designed to meet your unique needs.",
        "address1": "5430 S Biscay Cir",
        "address2": None,
        "stateCountry": "CO",
        "city": "Centennial",
        "postalCode": "80015",
        "county": "Arapahoe",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.767363,
        "latitude": 39.617865,
        "googlePlaceId": None,
        "referenceId": "97",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b3471b77-e849-47b6-89c9-b44127aaafb5",
        "name": "East Tennessee Fingerprinting",
        "displayName": "Printscan Authorized Fingerprint Service Center - Maryville, TN",
        "description": None,
        "metaDescription": "Choose PrintScan in Maryville, Tennessee, for superior Live Scan and Fingerprinting services. Rely on our modern technology for consistent accuracy and dependable results.",
        "notes": "Choose PrintScan in Maryville, Tennessee, for superior Live Scan and Fingerprinting services. Rely on our modern technology for consistent accuracy and dependable results.",
        "address1": "2146 Big Springs Rd",
        "address2": "Unit B",
        "stateCountry": "TN",
        "city": "Maryville",
        "postalCode": "37801",
        "county": "Monroe",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -84.034471,
        "latitude": 35.749218,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": "2000-01-01T14:30:00-05:00",
                "timeResume": "2000-01-01T15:30:00-05:00",
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": "2000-01-01T14:30:00-05:00",
                "timeResume": "2000-01-01T15:30:00-05:00",
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": "2000-01-01T14:30:00-05:00",
                "timeResume": "2000-01-01T15:30:00-05:00",
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": "2000-01-01T14:30:00-05:00",
                "timeResume": "2000-01-01T15:30:00-05:00",
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": "2000-01-01T14:30:00-05:00",
                "timeResume": "2000-01-01T15:30:00-05:00",
                "timeClose": "2000-01-01T18:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "85e0ae2e-e720-4b77-92c2-b7c01fc30d04",
        "name": "YMCA Snow Mountain Ranch (Open Thursday)",
        "displayName": "PrintScan | YMCA Snow Mountain Ranch (Open Thursday) - Granby, CO",
        "description": "Check-in at Guest Registration",
        "metaDescription": "Experience top-notch Live Scan and Fingerprinting services at PrintScan in Granby, Colorado. Our team of experts ensures quick, accurate, and reliable results for all your identification needs. Trust PrintScan Granby for secure and efficient services.",
        "notes": "Experience top-notch Live Scan and Fingerprinting services at PrintScan in Granby, Colorado. Our team of experts ensures quick, accurate, and reliable results for all your identification needs. Trust PrintScan Granby for secure and efficient services.",
        "address1": "1101 Co Rd 53",
        "address2": None,
        "stateCountry": "CO",
        "city": "Granby",
        "postalCode": "80446",
        "county": "Grand",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -105.941427,
        "latitude": 39.986841,
        "googlePlaceId": None,
        "referenceId": "125",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "ab4a0c73-05b0-4524-b9ff-b7c43c04ae0d",
        "name": "Logan County Chamber Sterling (Open Wednesday)",
        "displayName": "PrintScan | Logan County Chamber Sterling (Open Wednesday) - Sterling, CO",
        "description": "",
        "metaDescription": "Discover the premier provider of Live Scan and Fingerprinting services in Sterling, Colorado. PrintScan Sterling delivers fast, precise, and dependable results for all your identification requirements. Choose PrintScan for a secure and efficient experience.",
        "notes": "Discover the premier provider of Live Scan and Fingerprinting services in Sterling, Colorado. PrintScan Sterling delivers fast, precise, and dependable results for all your identification requirements. Choose PrintScan for a secure and efficient experience.",
        "address1": "109 N Front St",
        "address2": None,
        "stateCountry": "CO",
        "city": "Sterling",
        "postalCode": "80751",
        "county": "Logan",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -103.206394,
        "latitude": 40.623353,
        "googlePlaceId": None,
        "referenceId": "40",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "599c80f4-203e-461e-bace-ba24c83537d6",
        "name": "All in One Diagnostics LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Avon Park, FL",
        "description": None,
        "metaDescription": "Discover PrintScan Avon Park, Florida - your top choice for Live Scan and Fingerprinting services. Experience our efficient, reliable, and secure solutions, custom-made to suit your individual needs.",
        "notes": "Discover PrintScan Avon Park, Florida - your top choice for Live Scan and Fingerprinting services. Experience our efficient, reliable, and secure solutions, custom-made to suit your individual needs.",
        "address1": "1505 N Lake Avenue",
        "address2": None,
        "stateCountry": "FL",
        "city": "Avon Park",
        "postalCode": "33825",
        "county": "Polk",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.502581,
        "latitude": 27.614322,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T15:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T15:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T15:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T15:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T15:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b6e2d5d6-9437-4936-b9d5-baca40909262",
        "name": "ARCPoint Labs of Lexington",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Lexington, KY",
        "description": None,
        "metaDescription": "Welcome to PrintScan Lexington, Kentucky, your reliable source for Live Scan and Fingerprinting services. We provide quick, precise, and secure identification solutions to suit your individual requirements.",
        "notes": "Welcome to PrintScan Lexington, Kentucky, your reliable source for Live Scan and Fingerprinting services. We provide quick, precise, and secure identification solutions to suit your individual requirements.",
        "address1": "152 Tiverton Way",
        "address2": "120",
        "stateCountry": "KY",
        "city": "Lexington",
        "postalCode": "40503",
        "county": "Fayette",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -84.532909,
        "latitude": 37.980938,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:45:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:45:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:45:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:45:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:30:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "48df74a8-ffa5-4976-92bb-bacb244f668b",
        "name": "United Packaging & Shipping",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- McAlester, OK",
        "description": None,
        "metaDescription": "Experience fast and reliable Live Scan and Fingerprinting services at PrintScan in McAlester, Oklahoma. Our professional team ensures accurate results for all your identification needs. Trust PrintScan McAlester, your local solution for all fingerprinting services.",
        "notes": "Experience fast and reliable Live Scan and Fingerprinting services at PrintScan in McAlester, Oklahoma. Our professional team ensures accurate results for all your identification needs. Trust PrintScan McAlester, your local solution for all fingerprinting services.",
        "address1": "125 South Main Street",
        "address2": None,
        "stateCountry": "OK",
        "city": "McAlester",
        "postalCode": "74501",
        "county": "Pittsburg",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -95.769918,
        "latitude": 34.930152,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:45:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:45:00-06:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:45:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:45:00-06:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:45:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:45:00-06:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:45:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:45:00-06:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:45:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T17:45:00-06:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "71cdf590-2c26-453c-80c9-bd11284e80d1",
        "name": "Dolores School District RE-4A (Open Wednesday)",
        "displayName": "PrintScan | Dolores School District RE-4A (Open Wednesday) - Dolores, CO",
        "description": "",
        "metaDescription": "Choose PrintScan in Dolores, Colorado for superior Live Scan and Fingerprinting services. Our dedicated team provides swift, accurate, and reliable results, meeting all your identification needs. Trust in PrintScan Dolores for a secure and streamlined process.",
        "notes": "Choose PrintScan in Dolores, Colorado for superior Live Scan and Fingerprinting services. Our dedicated team provides swift, accurate, and reliable results, meeting all your identification needs. Trust in PrintScan Dolores for a secure and streamlined process.",
        "address1": "100 N 6th St",
        "address2": None,
        "stateCountry": "CO",
        "city": "Dolores",
        "postalCode": "81323",
        "county": "Montezuma",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -108.502514,
        "latitude": 37.474501,
        "googlePlaceId": None,
        "referenceId": "114",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "1d14c59f-bb8d-40f7-a1a2-c1ae2219de44",
        "name": "ANB Wellness, Inc. dba ARCPoint Labs of Rock Hill",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Rock Hill, SC",
        "description": None,
        "metaDescription": "Experience top-notch Live Scan and Fingerprinting services at PrintScan in Rock Hill, South Carolina. We offer secure, efficient, and reliable identification solutions to cater to your unique needs.",
        "notes": "Experience top-notch Live Scan and Fingerprinting services at PrintScan in Rock Hill, South Carolina. We offer secure, efficient, and reliable identification solutions to cater to your unique needs.",
        "address1": "725 Cherry Road",
        "address2": "Suite 157A",
        "stateCountry": "SC",
        "city": "Rock Hill",
        "postalCode": "29732",
        "county": "York",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.027761,
        "latitude": 34.945525,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T13:30:00-05:00",
                "timeClose": "2000-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T13:30:00-05:00",
                "timeClose": "2000-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T13:30:00-05:00",
                "timeClose": "2000-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T13:30:00-05:00",
                "timeClose": "2000-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T13:30:00-05:00",
                "timeClose": "2000-01-01T17:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "01eeff1f-c3dd-43a5-b11e-c38e2dd2ad8a",
        "name": "Westminster College Hill Library (Open Mon & Thurs)",
        "displayName": "PrintScan | Westminster College Hill Library (Open Mon & Thurs) - Westminster, CO",
        "description": "Check-in with Customer Service at Appointment",
        "metaDescription": "Trust PrintScan in Westminster, Colorado for your Live Scan and Fingerprinting needs. We deliver secure, efficient, and top-quality fingerprinting services, ensuring your complete satisfaction.",
        "notes": "Trust PrintScan in Westminster, Colorado for your Live Scan and Fingerprinting needs. We deliver secure, efficient, and top-quality fingerprinting services, ensuring your complete satisfaction.",
        "address1": "3705 W 112th Ave",
        "address2": None,
        "stateCountry": "CO",
        "city": "Westminster",
        "postalCode": "80031",
        "county": "Jefferson",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -105.040125,
        "latitude": 39.901159,
        "googlePlaceId": None,
        "referenceId": "71",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "38ac6a36-94c8-48b4-b999-c61253742b1f",
        "name": "USA Occupational Services LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Buffalo, NY",
        "description": None,
        "metaDescription": "Welcome to PrintScan Buffalo, New York - your go-to destination for Live Scan and Fingerprinting services. Benefit from our fast, trustworthy, and confidential solutions, specifically designed to cater to your unique requirements.",
        "notes": "Welcome to PrintScan Buffalo, New York - your go-to destination for Live Scan and Fingerprinting services. Benefit from our fast, trustworthy, and confidential solutions, specifically designed to cater to your unique requirements.",
        "address1": "327 Niagara Street",
        "address2": "Suite 9",
        "stateCountry": "NY",
        "city": "Buffalo",
        "postalCode": "14201",
        "county": "Erie",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -78.884302,
        "latitude": 42.893366,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T15:00:00-05:00",
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T15:00:00-05:00",
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T15:00:00-05:00",
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T15:00:00-05:00",
                "timeClose": "2000-01-01T18:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T15:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-05:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T13:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "54152875-f656-4649-a2de-c8a4459efc2f",
        "name": "Upper Pine River Fire Protection District Bayfield (Open Tuesday)",
        "displayName": "PrintScan | Upper Pine River Fire Protection District Bayfield (Open Tuesday) - Bayfield, CO",
        "description": "",
        "metaDescription": "Rely on PrintScan in Bayfield, Colorado for exceptional Live Scan and Fingerprinting services. Our skilled team delivers quick, precise, and trustworthy results for all your identification requirements. Choose PrintScan Bayfield for a secure and efficient identification solution.",
        "notes": "Rely on PrintScan in Bayfield, Colorado for exceptional Live Scan and Fingerprinting services. Our skilled team delivers quick, precise, and trustworthy results for all your identification requirements. Choose PrintScan Bayfield for a secure and efficient identification solution.",
        "address1": "515 Sower Dr",
        "address2": None,
        "stateCountry": "CO",
        "city": "Bayfield",
        "postalCode": "81122",
        "county": "La Plata",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -107.601623,
        "latitude": 37.235943,
        "googlePlaceId": None,
        "referenceId": "90",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "0166cad0-14c6-4afc-8d2a-cc3c135ff5be",
        "name": "Inspiration Field La Junta (Open Tues-Thurs)",
        "displayName": "PrintScan | Inspiration Field La Junta (Open Tues-Thurs) - La Junta, CO",
        "description": "",
        "metaDescription": "Opt for PrintScan in La Junta, Colorado for unparalleled Live Scan and Fingerprinting services. Our proficient team ensures speedy, accurate, and reliable results to cater to all your identification needs. Trust in PrintScan La Junta for a secure and effective service.",
        "notes": "Opt for PrintScan in La Junta, Colorado for unparalleled Live Scan and Fingerprinting services. Our proficient team ensures speedy, accurate, and reliable results to cater to all your identification needs. Trust in PrintScan La Junta for a secure and effective service.",
        "address1": "612 Adams Ave",
        "address2": None,
        "stateCountry": "CO",
        "city": "La Junta",
        "postalCode": "81050",
        "county": "Otero",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -103.546662,
        "latitude": 37.978376,
        "googlePlaceId": None,
        "referenceId": "30",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "a4fbaf79-67e3-4a68-a33e-cdd4a84e8e24",
        "name": "1 Accord Solutions LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Tampa, FL",
        "description": None,
        "metaDescription": "Discover PrintScan in Tampa, Florida, your reliable choice for Live Scan and Fingerprinting services. Enjoy our efficient, dependable, and customized solutions created to fulfill your specific requirements.",
        "notes": "Discover PrintScan in Tampa, Florida, your reliable choice for Live Scan and Fingerprinting services. Enjoy our efficient, dependable, and customized solutions created to fulfill your specific requirements.",
        "address1": "13542 N Florida Avenue",
        "address2": "Suite 212",
        "stateCountry": "FL",
        "city": "Tampa",
        "postalCode": "33613",
        "county": "Hillsborough",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -82.459833,
        "latitude": 28.071832,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": "2000-01-01T14:30:00-05:00",
                "timeResume": "2000-01-01T15:30:00-05:00",
                "timeClose": "2000-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": "2000-01-01T14:30:00-05:00",
                "timeResume": "2000-01-01T15:30:00-05:00",
                "timeClose": "2000-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": "2000-01-01T14:30:00-05:00",
                "timeResume": "2000-01-01T15:30:00-05:00",
                "timeClose": "2000-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": "2000-01-01T14:30:00-05:00",
                "timeResume": "2000-01-01T15:30:00-05:00",
                "timeClose": "2000-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": "2000-01-01T14:30:00-05:00",
                "timeResume": "2000-01-01T15:30:00-05:00",
                "timeClose": "2000-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b9430d28-3e7a-4476-80e6-ce2978fb08ce",
        "name": "Telluride Wilkinson Public Library (Open Tues, Wed, Fri)",
        "displayName": "PrintScan | Telluride Wilkinson Public Library (Open Tues, Wed, Fri) - Telluride, CO",
        "description": "Wilkinson Public Library",
        "metaDescription": "Visit PrintScan in Telluride, Colorado for outstanding Live Scan and Fingerprinting services. Our expert team provides fast, precise, and dependable results for all your identification requirements. Choose PrintScan Telluride for a secure and efficient identification process.",
        "notes": "Visit PrintScan in Telluride, Colorado for outstanding Live Scan and Fingerprinting services. Our expert team provides fast, precise, and dependable results for all your identification requirements. Choose PrintScan Telluride for a secure and efficient identification process.",
        "address1": "100 W Pacific Ave",
        "address2": None,
        "stateCountry": "CO",
        "city": "Telluride",
        "postalCode": "81435",
        "county": "San Miguel",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -107.811448,
        "latitude": 37.936213,
        "googlePlaceId": None,
        "referenceId": "73",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "27c821e5-90bd-4a60-96ae-dd2bfca69b0e",
        "name": "Melody's Southwest Consortium",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- San Angelo, TX",
        "description": None,
        "metaDescription": "Explore PrintScan San Angelo, Texas - your premier provider for Live Scan and Fingerprinting services. Enjoy our swift, dependable, and secure solutions, tailored to meet your specific needs.",
        "notes": "Explore PrintScan San Angelo, Texas - your premier provider for Live Scan and Fingerprinting services. Enjoy our swift, dependable, and secure solutions, tailored to meet your specific needs.",
        "address1": "300 E 3rd Street",
        "address2": None,
        "stateCountry": "TX",
        "city": "San Angelo",
        "postalCode": "76903",
        "county": "Tom Green",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -100.433477,
        "latitude": 31.470524,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T12:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T12:00:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T12:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T12:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "0d8a1359-d7c8-4ea5-af47-e100d86757f0",
        "name": "Elite Testing Solutions Thornton (Open Mon-Thurs)",
        "displayName": "PrintScan | Elite Testing Solutions Thornton (Open Mon-Thurs) - Thornton, CO",
        "description": "Suite 201",
        "metaDescription": "Discover top-notch Live Scan and Fingerprinting services in Thornton, Colorado with PrintScan. Our dedicated team delivers precise and quick results for all your identification requirements. Choose PrintScan Thornton for your secure and efficient fingerprinting needs.",
        "notes": "Discover top-notch Live Scan and Fingerprinting services in Thornton, Colorado with PrintScan. Our dedicated team delivers precise and quick results for all your identification requirements. Choose PrintScan Thornton for your secure and efficient fingerprinting needs.",
        "address1": "9669 Huron St",
        "address2": None,
        "stateCountry": "CO",
        "city": "Thornton",
        "postalCode": "80260",
        "county": "Adams",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.997257,
        "latitude": 39.872211,
        "googlePlaceId": None,
        "referenceId": "41",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "09dd2cdc-66ca-4e97-bd9c-e2da3eba0206",
        "name": "Express It Mail Center Longmont (Open Mon-Sat)",
        "displayName": "PrintScan | Express It Mail Center Longmont (Open Mon-Sat) - Longmont, CO",
        "description": "Located in Suite 120",
        "metaDescription": "Visit PrintScan in Longmont, Colorado for exceptional Live Scan and Fingerprinting services. Our expert team provides swift, accurate, and dependable results, catering to all your identification needs. Choose PrintScan Longmont for a secure and effective identification process.",
        "notes": "Visit PrintScan in Longmont, Colorado for exceptional Live Scan and Fingerprinting services. Our expert team provides swift, accurate, and dependable results, catering to all your identification needs. Choose PrintScan Longmont for a secure and effective identification process.",
        "address1": "205 Ken Pratt Blvd",
        "address2": None,
        "stateCountry": "CO",
        "city": "Longmont",
        "postalCode": "80501",
        "county": "Boulder",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -105.095127,
        "latitude": 40.150739,
        "googlePlaceId": None,
        "referenceId": "91",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "547aa0ae-6556-4e21-80ff-e3982a26ea4e",
        "name": "Crowley County School District (Open Tues-Fri)",
        "displayName": "PrintScan | Crowley County School District (Open Tues-Fri) - Ordway, CO",
        "description": "Enter through the Main Entrance at Reception",
        "metaDescription": "Choose PrintScan in Ordway, Colorado for top-notch Live Scan and Fingerprinting services. Our skilled team ensures swift, accurate, and reliable results for all your identification needs. Rely on PrintScan Ordway for a secure and efficient identification experience.",
        "notes": "Choose PrintScan in Ordway, Colorado for top-notch Live Scan and Fingerprinting services. Our skilled team ensures swift, accurate, and reliable results for all your identification needs. Rely on PrintScan Ordway for a secure and efficient identification experience.",
        "address1": "1001 Main St",
        "address2": None,
        "stateCountry": "CO",
        "city": "Ordway",
        "postalCode": "81063",
        "county": "Crowley",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -103.755689,
        "latitude": 38.227553,
        "googlePlaceId": None,
        "referenceId": "93",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "8920a6b5-7149-ed11-ade6-e42aac775f09",
        "name": "Bear-2-Arm Tactical DBA: Bear Secure",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Fayetteville, GA",
        "description": "SUITE 607A - Please ring the bell upon arrival",
        "metaDescription": "Discover exceptional Live Scan and Fingerprinting services at PrintScan in Fayetteville, Georgia. Our skilled team ensures swift and precise results for all your identification tasks. Trust PrintScan Fayetteville, GA for your secure and efficient fingerprinting needs.",
        "notes": "Discover exceptional Live Scan and Fingerprinting services at PrintScan in Fayetteville, Georgia. Our skilled team ensures swift and precise results for all your identification tasks. Trust PrintScan Fayetteville, GA for your secure and efficient fingerprinting needs.",
        "address1": "101 Devant Street",
        "address2": "Suite 607A",
        "stateCountry": "GA",
        "city": "Fayetteville",
        "postalCode": "30215",
        "county": "Fayette",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -84.483827,
        "latitude": 33.449899,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-09-07T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-07T18:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-09-07T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-07T18:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-09-07T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-07T18:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-09-07T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-07T18:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-09-07T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-09-07T18:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b9e3c4b8-4e4a-ed11-ade6-e42aac775f09",
        "name": "GM Defense LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Pleasanton, CA",
        "description": "Please Contact us for After-Hours Appointments",
        "metaDescription": "Find premier Live Scan and Fingerprinting services at PrintScan in Pleasanton, California. Our dedicated team delivers fast and accurate results for all your identification requirements. Rely on PrintScan Pleasanton, CA for trustworthy and prompt fingerprinting solutions.",
        "notes": "Find premier Live Scan and Fingerprinting services at PrintScan in Pleasanton, California. Our dedicated team delivers fast and accurate results for all your identification requirements. Rely on PrintScan Pleasanton, CA for trustworthy and prompt fingerprinting solutions.",
        "address1": "4125 Mohr Ave",
        "address2": "Suite F",
        "stateCountry": "CA",
        "city": "Pleasanton",
        "postalCode": "94566",
        "county": "Alameda",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -121.873366,
        "latitude": 37.682262,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T10:00:00-07:00",
                "timeLunch": "2000-01-01T12:00:00-07:00",
                "timeResume": "2000-01-01T17:00:00-07:00",
                "timeClose": "2000-01-01T18:30:00-07:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:00:00-07:00",
                "timeLunch": "2000-01-01T12:00:00-07:00",
                "timeResume": "2000-01-01T17:30:00-07:00",
                "timeClose": "2000-01-01T20:30:00-07:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:00:00-07:00",
                "timeLunch": "2000-01-01T12:00:00-07:00",
                "timeResume": "2000-01-01T17:00:00-07:00",
                "timeClose": "2000-01-01T18:30:00-07:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:00:00-07:00",
                "timeLunch": "2000-01-01T12:00:00-07:00",
                "timeResume": "2000-01-01T17:30:00-07:00",
                "timeClose": "2000-01-01T20:30:00-07:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00-07:00",
                "timeLunch": "2000-01-01T12:00:00-07:00",
                "timeResume": "2000-01-01T17:00:00-07:00",
                "timeClose": "2000-01-01T18:30:00-07:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-06-26T12:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:00:00-07:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b7c709e0-c6e8-ec11-b47a-e42aac777c47",
        "name": "ABC LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Miami, FL",
        "description": "Second Floor corner office, Next to Wise Choice Tutoring.",
        "metaDescription": "Explore PrintScan in Miami, Florida, your premier choice for advanced Live Scan and Fingerprinting services. Benefit from our swift, secure, and dependable fingerprinting processes at PrintScan Miami today.",
        "notes": "Explore PrintScan in Miami, Florida, your premier choice for advanced Live Scan and Fingerprinting services. Benefit from our swift, secure, and dependable fingerprinting processes at PrintScan Miami today.",
        "address1": "10481 N Kendall Drive",
        "address2": "Suite D201",
        "stateCountry": "FL",
        "city": "Miami",
        "postalCode": "33176",
        "county": "Miami-Dade",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -80.363018,
        "latitude": 25.687538,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-29T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-29T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-29T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-29T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-29T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "f4b76460-b5ec-ec11-b47a-e42aac777c47",
        "name": "Premier Notary and Fingerprinting",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Orlando, FL",
        "description": None,
        "metaDescription": "Choose PrintScan in Orlando, Florida, for all your Live Scan and Fingerprinting needs. Experience our commitment to providing fast, secure, and reliable services that prioritize your satisfaction and security.",
        "notes": "Choose PrintScan in Orlando, Florida, for all your Live Scan and Fingerprinting needs. Experience our commitment to providing fast, secure, and reliable services that prioritize your satisfaction and security.",
        "address1": "20 N Orange Ave",
        "address2": "Ste 1100",
        "stateCountry": "FL",
        "city": "Orlando",
        "postalCode": "32801",
        "county": "Orange",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.379376,
        "latitude": 28.542514,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-07-24T12:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-24T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-07-24T12:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-24T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "2340b463-fcf6-ec11-b47a-e42aac777c47",
        "name": "Jace Laboratories & Screening LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Jacksonville, FL",
        "description": "Located inside Regency Business Center, Building #3",
        "metaDescription": "Visit PrintScan in Jacksonville, Florida, your reliable choice for premier Live Scan and Fingerprinting services. Benefit from our fast, secure, and dependable solutions tailored to meet your unique needs.",
        "notes": "Visit PrintScan in Jacksonville, Florida, your reliable choice for premier Live Scan and Fingerprinting services. Benefit from our fast, secure, and dependable solutions tailored to meet your unique needs.",
        "address1": "9951 Atlantic Blvd",
        "address2": "Suite 322",
        "stateCountry": "FL",
        "city": "Jacksonville",
        "postalCode": "32225",
        "county": "Duval",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.541602,
        "latitude": 30.323921,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2000-01-01T15:00:00-05:00",
                "timeClose": "2000-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T11:00:00-05:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2023-07-13T15:00:00+00:00",
                "timeClose": "2023-07-13T18:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2023-07-13T15:00:00+00:00",
                "timeClose": "2000-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2023-07-13T15:00:00+00:00",
                "timeClose": "2000-01-01T17:00:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:00:00-05:00",
                "timeLunch": "2000-01-01T13:00:00-05:00",
                "timeResume": "2023-07-13T15:00:00+00:00",
                "timeClose": "2000-01-01T17:00:00-05:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "4be2fa13-07fe-ec11-b47a-e42aac777c47",
        "name": "Patrona Corporation",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Dover,NH",
        "description": None,
        "metaDescription": "Experience the best in Live Scan and Fingerprinting services at PrintScan in Dover, New Hampshire. We offer cutting-edge technology for precise, dependable results. Choose PrintScan Dover for your secure and swift fingerprinting requirements.",
        "notes": "Experience the best in Live Scan and Fingerprinting services at PrintScan in Dover, New Hampshire. We offer cutting-edge technology for precise, dependable results. Choose PrintScan Dover for your secure and swift fingerprinting requirements.",
        "address1": "383 Central Ave",
        "address2": "Suite 1",
        "stateCountry": "NH",
        "city": "Dover",
        "postalCode": "03820",
        "county": "Strafford",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -70.873051,
        "latitude": 43.196017,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2022-07-08T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-07-08T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-29T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-29T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2022-07-08T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-07-31T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-31T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-29T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "43c7c6f4-5701-ed11-b47a-e42aac777c47",
        "name": "Postal Place PDX",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Portland Kiosk Location",
        "description": "**MASKS ARE REQUIRED FOR ALL FINGERPRINT APPOINTMENTS** - Use the door to the right of the convenience store",
        "metaDescription": "Visit PrintScan in Portland, Oregon, your trusted destination for Live Scan and Fingerprinting services. Experience our efficient, precise, and secure identity confirmation solutions, tailored to meet your unique requirements.",
        "notes": "Visit PrintScan in Portland, Oregon, your trusted destination for Live Scan and Fingerprinting services. Experience our efficient, precise, and secure identity confirmation solutions, tailored to meet your unique requirements.",
        "address1": "10350 North Vancouver Way",
        "address2": None,
        "stateCountry": "OR",
        "city": "Portland",
        "postalCode": "97217",
        "county": "Multnomah",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -122.669381,
        "latitude": 45.597782,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:45:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:45:00-07:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:45:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:45:00-07:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:45:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:45:00-07:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:45:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:45:00-07:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:45:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:45:00-07:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T09:15:00-07:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T13:45:00-07:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "738f2587-3609-ed11-b47a-e42aac777c47",
        "name": "The UPS Store 4766 - (Downtown NYC)",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Downtown NYC Kiosk Location",
        "description": "UPS Store located between Fulton St. & John St. (Fulton St. Subway Station)",
        "metaDescription": "Experience top-notch Live Scan and Fingerprinting services at PrintScan in New York, New York. We offer secure, efficient, and reliable identification solutions to meet your unique needs.",
        "notes": "Experience top-notch Live Scan and Fingerprinting services at PrintScan in New York, New York. We offer secure, efficient, and reliable identification solutions to meet your unique needs.",
        "address1": "82 Nassau Street",
        "address2": None,
        "stateCountry": "NY",
        "city": "New York",
        "postalCode": "10038",
        "county": "New York",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -74.007897,
        "latitude": 40.709763,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2022-07-26T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-07-26T18:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2022-07-26T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-07-26T18:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2022-07-26T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-07-26T18:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2022-07-26T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-07-26T18:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2022-07-26T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-07-26T18:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "7fed0b9b-3709-ed11-b47a-e42aac777c47",
        "name": "Copy Experts",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Uptown NYC Kiosk Location",
        "description": None,
        "metaDescription": "Experience top-notch Live Scan and Fingerprinting services at PrintScan in New York, New York. We offer secure, efficient, and reliable identification solutions to meet your unique needs.",
        "notes": "Experience top-notch Live Scan and Fingerprinting services at PrintScan in New York, New York. We offer secure, efficient, and reliable identification solutions to meet your unique needs.",
        "address1": "2424 Broadway",
        "address2": None,
        "stateCountry": "NY",
        "city": "New York",
        "postalCode": "10024",
        "county": "New York",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -73.976803,
        "latitude": 40.790313,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 0,
                "timeOpen": "2023-07-28T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-28T18:00:00+00:00"
            },
            {
                "dayOfWeek": 1,
                "timeOpen": "2022-07-27T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-07-27T18:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2022-07-27T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-07-27T18:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2022-07-27T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-07-27T18:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2022-07-27T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-07-27T18:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2022-07-27T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-07-27T18:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-07-28T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-28T18:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "578987af-b80d-ed11-b47a-e42aac777c47",
        "name": "Onyx Fingerprinting",
        "displayName": "PrintScan - Authorized Fingerprint Service Center",
        "description": "Inside of the HDC Building",
        "metaDescription": "Discover exceptional Live Scan and Fingerprinting services at PrintScan in Hammond, Indiana. Leveraging advanced technology, we deliver accurate and reliable results. Choose PrintScan Hammond for all your secure, efficient fingerprinting needs.",
        "notes": "Discover exceptional Live Scan and Fingerprinting services at PrintScan in Hammond, Indiana. Leveraging advanced technology, we deliver accurate and reliable results. Choose PrintScan Hammond for all your secure, efficient fingerprinting needs.",
        "address1": "5233 Hohman Avenue",
        "address2": "Suite 101",
        "stateCountry": "IN",
        "city": "Hammond",
        "postalCode": "46320",
        "county": "Lake",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -87.521371,
        "latitude": 41.618015,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-07-28T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-07-28T16:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2022-09-30T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-09-30T16:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2022-09-30T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-09-30T16:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2022-09-30T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-09-30T16:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2022-09-30T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-09-30T16:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "e0c4fd4b-45d8-ec11-b656-e42aac778fc7",
        "name": "Integrity Financial Services LLC DBA IMS Screening",
        "displayName": "PrintScan - Authorized Fingerprint Service Center",
        "description": None,
        "metaDescription": "Get superior Live Scan and Fingerprinting services at PrintScan in Desoto, Texas. Our expert team provides fast and accurate results, making us the preferred choice for all your identification needs. Rely on PrintScan Desoto for all your secure fingerprinting solutions.",
        "notes": "Get superior Live Scan and Fingerprinting services at PrintScan in Desoto, Texas. Our expert team provides fast and accurate results, making us the preferred choice for all your identification needs. Rely on PrintScan Desoto for all your secure fingerprinting solutions.",
        "address1": "1301 E Parkerville Rd",
        "address2": "Suite A5",
        "stateCountry": "TX",
        "city": "DeSoto",
        "postalCode": "75115",
        "county": "Dallas",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -96.827144,
        "latitude": 32.575663,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-01T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-01T14:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-01T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-01T14:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-01T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-01T14:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-01T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-01T14:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-01T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-01T14:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "ccfeab5a-d4e5-ec11-b656-e42aac778fc7",
        "name": "My Office (Lake Highlands)",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Dallas Kiosk Location",
        "description": "**THIS LOCATION REQUIRES MASKS TO BE WORN ON SITE**",
        "metaDescription": "Turn to PrintScan in Dallas, Texas, for exceptional Live Scan and Fingerprinting services. Experience our dedication to providing fast, secure, and reliable solutions that meet your specific needs.",
        "notes": "Turn to PrintScan in Dallas, Texas, for exceptional Live Scan and Fingerprinting services. Experience our dedication to providing fast, secure, and reliable solutions that meet your specific needs.",
        "address1": "10228 East Northwest Highway",
        "address2": None,
        "stateCountry": "TX",
        "city": "Dallas",
        "postalCode": "75238",
        "county": "Dallas",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -96.709538,
        "latitude": 32.863803,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2022-06-06T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-06-06T15:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2022-06-06T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-06-06T15:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2022-06-06T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-06-06T15:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2022-06-06T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-06-06T15:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2022-06-06T11:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-06-06T15:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "8b5c6315-f934-ed11-ae83-e42aac779987",
        "name": "Edwards & Roberts LLC",
        "displayName": "Printscan Authorized Fingerprint Service Center - El Paso, TX",
        "description": None,
        "metaDescription": "Experience fast and reliable Live Scan and Fingerprinting services in El Paso, Texas with PrintScan. We're committed to providing top-notch security solutions for your identification needs.",
        "notes": "Experience fast and reliable Live Scan and Fingerprinting services in El Paso, Texas with PrintScan. We're committed to providing top-notch security solutions for your identification needs.",
        "address1": "9611B Acer Ave.",
        "address2": "Suite 122",
        "stateCountry": "TX",
        "city": "El Paso",
        "postalCode": "79925",
        "county": "El Paso",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -106.357447,
        "latitude": 31.766733,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T09:30:00-07:00",
                "timeLunch": "2000-01-01T13:30:00-07:00",
                "timeResume": "2000-01-01T14:30:00-07:00",
                "timeClose": "2000-01-01T18:00:00-07:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T09:30:00-07:00",
                "timeLunch": "2000-01-01T13:30:00-07:00",
                "timeResume": "2000-01-01T14:30:00-07:00",
                "timeClose": "2000-01-01T18:00:00-07:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T09:30:00-07:00",
                "timeLunch": "2000-01-01T13:30:00-07:00",
                "timeResume": "2000-01-01T14:30:00-07:00",
                "timeClose": "2000-01-01T18:00:00-07:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T09:30:00-07:00",
                "timeLunch": "2000-01-01T13:30:00-07:00",
                "timeResume": "2000-01-01T14:30:00-07:00",
                "timeClose": "2000-01-01T18:00:00-07:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T09:30:00-07:00",
                "timeLunch": "2000-01-01T13:30:00-07:00",
                "timeResume": "2000-01-01T14:30:00-07:00",
                "timeClose": "2000-01-01T17:45:00-07:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "0b88b641-e2a9-ec11-997e-e42aac77a34a",
        "name": "Midwest Fingerprinting and More LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center",
        "description": "Midwest Fingerprinting and More",
        "metaDescription": "Experience high-quality Live Scan and Fingerprinting services at PrintScan in St. Louis, Missouri. Enjoy our quick, reliable, and expert services, customized to fit your individual needs. Choose PrintScan St. Louis, MO for all your identification and security solutions.",
        "notes": "Experience high-quality Live Scan and Fingerprinting services at PrintScan in St. Louis, Missouri. Enjoy our quick, reliable, and expert services, customized to fit your individual needs. Choose PrintScan St. Louis, MO for all your identification and security solutions.",
        "address1": "7320 Florissant Road",
        "address2": "Unit 1D",
        "stateCountry": "MO",
        "city": "St. Louis",
        "postalCode": "63121-2526",
        "county": "Saint Louis",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -90.296760,
        "latitude": 38.704503,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-04-12T08:30:00+00:00",
                "timeLunch": "2023-04-12T12:00:00+00:00",
                "timeResume": "2023-04-12T13:30:00+00:00",
                "timeClose": "2023-04-12T17:30:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-04-12T08:30:00+00:00",
                "timeLunch": "2023-04-12T12:00:00+00:00",
                "timeResume": "2023-04-12T13:30:00+00:00",
                "timeClose": "2023-04-12T17:30:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-04-12T08:30:00+00:00",
                "timeLunch": "2023-04-12T12:00:00+00:00",
                "timeResume": "2000-01-01T14:30:00-06:00",
                "timeClose": "2023-04-12T17:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-04-12T08:30:00+00:00",
                "timeLunch": "2023-04-12T12:00:00+00:00",
                "timeResume": "2023-04-12T13:30:00+00:00",
                "timeClose": "2023-04-12T17:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-04-12T08:30:00+00:00",
                "timeLunch": "2023-04-12T12:00:00+00:00",
                "timeResume": "2023-04-12T13:30:00+00:00",
                "timeClose": "2023-04-12T17:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "d4b93d44-7fab-ec11-997e-e42aac77a34a",
        "name": "North Market Chiropractic Clinic",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Shreveport, LA",
        "description": "Across the street from AutoZone",
        "metaDescription": "Choose PrintScan in Shreveport, Louisiana for top-notch Live Scan and Fingerprinting services. Our dedication to speed and precision in identification services sets us apart. Trust in PrintScan Shreveport for all your fingerprinting requirements.",
        "notes": "Choose PrintScan in Shreveport, Louisiana for top-notch Live Scan and Fingerprinting services. Our dedication to speed and precision in identification services sets us apart. Trust in PrintScan Shreveport for all your fingerprinting requirements.",
        "address1": "1850 Nelson Street",
        "address2": "Suite D",
        "stateCountry": "LA",
        "city": "Shreveport",
        "postalCode": "71107",
        "county": "Caddo",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -93.777096,
        "latitude": 32.544041,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-08-17T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-17T15:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-08-17T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-17T15:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-08-17T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-17T15:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-08-17T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-17T15:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-08-17T09:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-08-17T13:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "55b69fb9-f9b0-ec11-997e-e42aac77a34a",
        "name": "DCF Guns",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Castle Rock, CO",
        "description": None,
        "metaDescription": "Discover PrintScan in Castle Rock, Colorado, the leading provider of exceptional Live Scan and Fingerprinting services. We offer secure, quick, and trustworthy solutions for all your identification and verification requirements.",
        "notes": "Discover PrintScan in Castle Rock, Colorado, the leading provider of exceptional Live Scan and Fingerprinting services. We offer secure, quick, and trustworthy solutions for all your identification and verification requirements.",
        "address1": "1155 Park Street",
        "address2": None,
        "stateCountry": "CO",
        "city": "Castle Rock",
        "postalCode": "80109",
        "county": "Douglas",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.866943,
        "latitude": 39.381707,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 0,
                "timeOpen": "2023-01-27T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-01-27T19:00:00+00:00"
            },
            {
                "dayOfWeek": 1,
                "timeOpen": "2023-01-27T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-01-27T19:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2023-01-27T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-01-27T19:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2023-01-27T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-01-27T19:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-01-27T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-01-27T19:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2023-01-27T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-01-27T19:00:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2023-01-27T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-01-27T19:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "d7c9d10d-c5b1-ec11-997e-e42aac77a34a",
        "name": "Gifted Hands Notary & Signing Services LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center",
        "description": None,
        "metaDescription": "Rely on PrintScan in Jonesboro, Georgia for high-quality Live Scan and Fingerprinting services. We're dedicated to providing secure, fast, and dependable identification solutions for our clients.",
        "notes": "Rely on PrintScan in Jonesboro, Georgia for high-quality Live Scan and Fingerprinting services. We're dedicated to providing secure, fast, and dependable identification solutions for our clients.",
        "address1": "1351 Oakbrook Drive",
        "address2": "Suite 100",
        "stateCountry": "GA",
        "city": "Norcross",
        "postalCode": "30093",
        "county": "Gwinnett",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -84.187306,
        "latitude": 33.917074,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2022-07-11T09:30:00+00:00",
                "timeLunch": "2022-07-11T12:00:00+00:00",
                "timeResume": "2022-07-11T13:00:00+00:00",
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2022-07-11T09:30:00+00:00",
                "timeLunch": "2022-07-11T12:00:00+00:00",
                "timeResume": "2022-07-11T13:00:00+00:00",
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2022-07-11T09:00:00+00:00",
                "timeLunch": "2022-07-11T12:00:00+00:00",
                "timeResume": "2022-07-11T13:00:00+00:00",
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2022-07-11T09:30:00+00:00",
                "timeLunch": "2022-07-11T12:00:00+00:00",
                "timeResume": "2022-07-11T13:00:00+00:00",
                "timeClose": "2000-01-01T16:30:00-05:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2022-04-05T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-04-05T13:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "9f378e50-aec0-ec11-997e-e42aac77a34a",
        "name": "Colorado Springs Fingerprinting/The Mail Center",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Colorado Springs, CO",
        "description": None,
        "metaDescription": "Visit PrintScan in Colorado Springs, Colorado, your premier choice for comprehensive Live Scan and Fingerprinting services. Benefit from our secure, swift, and trustworthy solutions for all your identification and verification needs.",
        "notes": "Visit PrintScan in Colorado Springs, Colorado, your premier choice for comprehensive Live Scan and Fingerprinting services. Benefit from our secure, swift, and trustworthy solutions for all your identification and verification needs.",
        "address1": "6547 N Academy Blvd",
        "address2": None,
        "stateCountry": "CO",
        "city": "Colorado Springs",
        "postalCode": "80918",
        "county": "El Paso",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.792822,
        "latitude": 38.926942,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2022-04-20T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-04-20T17:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2022-04-20T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-04-20T17:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2022-04-20T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-04-20T17:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2022-04-20T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-04-20T17:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2022-04-20T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-04-20T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "37c6112d-9ec1-ec11-997e-e42aac77a34a",
        "name": "Infinite DOT Testing Center LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center - Orlando, FL",
        "description": None,
        "metaDescription": "Choose PrintScan in Orlando, Florida, for all your Live Scan and Fingerprinting needs. Experience our commitment to providing fast, secure, and reliable services that prioritize your satisfaction and security.",
        "notes": "Choose PrintScan in Orlando, Florida, for all your Live Scan and Fingerprinting needs. Experience our commitment to providing fast, secure, and reliable services that prioritize your satisfaction and security.",
        "address1": "6100 Lake Ellenor Drive",
        "address2": "Suite 151",
        "stateCountry": "FL",
        "city": "Orlando",
        "postalCode": "32809",
        "county": "Orange",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -81.404458,
        "latitude": 28.468722,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2022-12-13T10:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-12-13T20:00:00+00:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2022-04-21T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-04-21T20:00:00+00:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2022-04-21T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-04-21T20:00:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2022-04-21T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-04-21T20:00:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2022-12-13T08:00:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-12-13T17:00:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "35033f11-5dcd-ec11-997e-e42aac77a34a",
        "name": "Zink Arms LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center - Nottingham, MD",
        "description": None,
        "metaDescription": "Opt for PrintScan in Nottingham, Maryland for premier Live Scan and Fingerprinting services. Our dedicated team provides quick, accurate, and reliable identification solutions for your convenience.",
        "notes": "Opt for PrintScan in Nottingham, Maryland for premier Live Scan and Fingerprinting services. Our dedicated team provides quick, accurate, and reliable identification solutions for your convenience.",
        "address1": "9512 Belair Road",
        "address2": None,
        "stateCountry": "MD",
        "city": "Nottingham",
        "postalCode": "21236",
        "county": "Baltimore",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -76.468162,
        "latitude": 39.409433,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 3,
                "timeOpen": "2022-10-26T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-10-26T17:30:00+00:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2023-05-17T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2023-05-17T16:30:00+00:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2022-10-26T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-10-26T17:30:00+00:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2022-10-26T10:30:00+00:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2022-10-26T17:30:00+00:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "e34e743d-914a-48b0-8df4-e6bd3ee4d229",
        "name": "Starpoint Canon City (Open Mon & Wed)",
        "displayName": "PrintScan | Starpoint Canon City (Open Mon & Wed) - Cañon City, CO",
        "description": "Spin Early Childhood Facility",
        "metaDescription": "Discover PrintScan in Canon City, Colorado, your trusted provider for Live Scan and Fingerprinting services. Experience fast, accurate, and reliable solutions tailored to meet your identification needs.",
        "notes": "Discover PrintScan in Canon City, Colorado, your trusted provider for Live Scan and Fingerprinting services. Experience fast, accurate, and reliable solutions tailored to meet your identification needs.",
        "address1": "1339 Elm Ave",
        "address2": None,
        "stateCountry": "CO",
        "city": "Cañon City",
        "postalCode": "81212",
        "county": None,
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -105.219965,
        "latitude": 38.426326,
        "googlePlaceId": None,
        "referenceId": "81",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "0dec45d3-b2bb-411f-aac6-e7f8f230c8d1",
        "name": "ARCPoint Labs of Lancaster",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Lancaster, CA",
        "description": None,
        "metaDescription": "Discover top-tier Live Scan and Fingerprinting services at PrintScan in Lancaster, California. Our state-of-the-art technology guarantees accurate, reliable results. Choose PrintScan Lancaster, California for all your fingerprinting needs.",
        "notes": "Discover top-tier Live Scan and Fingerprinting services at PrintScan in Lancaster, California. Our state-of-the-art technology guarantees accurate, reliable results. Choose PrintScan Lancaster, California for all your fingerprinting needs.",
        "address1": "43823 10th Street W",
        "address2": None,
        "stateCountry": "CA",
        "city": "Lancaster",
        "postalCode": "93534",
        "county": "Los Angeles",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -118.148293,
        "latitude": 34.679425,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-08:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-08:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-08:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-08:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:30:00-08:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "58f3ed40-5a93-4300-acf7-e97124782aa6",
        "name": "Wiz Quiz Boulder (Open Mon-Fri)",
        "displayName": "PrintScan | Wiz Quiz Boulder (Open Mon-Fri) - Boulder, CO",
        "description": "Boulder is the only Wiz Quiz location any other Wiz Quiz is not providing fingerprinting",
        "metaDescription": "Get superior Live Scan and Fingerprinting services in Boulder, Colorado with PrintScan. Our expert team is committed to providing fast and accurate results for all your identification processes. Rely on PrintScan Boulder for secure, efficient, and reliable fingerprinting solutions.",
        "notes": "Get superior Live Scan and Fingerprinting services in Boulder, Colorado with PrintScan. Our expert team is committed to providing fast and accurate results for all your identification processes. Rely on PrintScan Boulder for secure, efficient, and reliable fingerprinting solutions.",
        "address1": "737 29th St #101",
        "address2": None,
        "stateCountry": "CO",
        "city": "Boulder",
        "postalCode": "80303",
        "county": "Boulder",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -105.256230,
        "latitude": 40.000950,
        "googlePlaceId": None,
        "referenceId": "4",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "806155b0-8f7d-45c4-9526-ebbd791cc95b",
        "name": "ARCpoint Labs of Humble",
        "displayName": "PrintScan Authorized Fingerprint Service Center- Humble, TX",
        "description": None,
        "metaDescription": "Discover PrintScan in Humble, Texas, your go-to source for exceptional Live Scan and Fingerprinting services. Benefit from our speedy, secure, and dependable fingerprinting solutions at PrintScan Humble today.",
        "notes": "Discover PrintScan in Humble, Texas, your go-to source for exceptional Live Scan and Fingerprinting services. Benefit from our speedy, secure, and dependable fingerprinting solutions at PrintScan Humble today.",
        "address1": "17903 W Lake Houston Pkwy",
        "address2": "Suite 204",
        "stateCountry": "TX",
        "city": "Humble",
        "postalCode": "77346",
        "county": "Harris",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -95.166423,
        "latitude": 29.979996,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:45:00-06:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:45:00-06:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:45:00-06:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:45:00-06:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T08:30:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T16:45:00-06:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "99c0be0f-9a7b-4e78-beb2-ef1bea34efda",
        "name": "Executive Investigations",
        "displayName": "PrintScan Authorized Fingerprint Service Center- Cheektowaga, NY",
        "description": None,
        "metaDescription": "Discover top-notch Live Scan and Fingerprinting services in Cheektowaga, New York with PrintScan. Your go-to provider for secure and efficient identity verification solutions.",
        "notes": "Discover top-notch Live Scan and Fingerprinting services in Cheektowaga, New York with PrintScan. Your go-to provider for secure and efficient identity verification solutions.",
        "address1": "1660 Kensington Avenue Suite 4",
        "address2": None,
        "stateCountry": "NY",
        "city": "Cheektowaga",
        "postalCode": "14215",
        "county": "Erie",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -78.795611,
        "latitude": 42.945675,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:00:00-04:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T14:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "89e8ed7c-4797-4f2f-96c4-ef33a51b5928",
        "name": "Ankur QA Location (No Slots Available)",
        "displayName": "PrintScan | Ankur QA Location (No Slots Available) - Portland, OR",
        "description": "",
        "metaDescription": "Explore PrintScan in Alamosa, Colorado, a leading destination for Live Scan and Fingerprinting services. Benefit from our precision, speed, and commitment to delivering top-notch identification solutions.",
        "notes": "Explore PrintScan in Alamosa, Colorado, a leading destination for Live Scan and Fingerprinting services. Benefit from our precision, speed, and commitment to delivering top-notch identification solutions.",
        "address1": "9585 SW Washington Square Rd",
        "address2": None,
        "stateCountry": "OR",
        "city": "Portland",
        "postalCode": "97223",
        "county": "Alamosa",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -122.781237,
        "latitude": 45.449787,
        "googlePlaceId": None,
        "referenceId": "144",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "70248be9-8fa8-4dea-bec4-f03343cc7314",
        "name": "Colorado Fingerprinting Boy Scouts, Denver Council (Open Wednesday)",
        "displayName": "PrintScan | Colorado Fingerprinting Boy Scouts, Denver Council (Open Wednesday) - Lakewood, CO",
        "description": "Enter at the \"Scout Shop\" on East end of the Building",
        "metaDescription": "Discover the premier Live Scan and Fingerprinting services in Lakewood, Colorado at PrintScan. We offer efficient, precise, and trustworthy solutions for all your identification requirements. Choose PrintScan Lakewood for your safety and security needs.",
        "notes": "Discover the premier Live Scan and Fingerprinting services in Lakewood, Colorado at PrintScan. We offer efficient, precise, and trustworthy solutions for all your identification requirements. Choose PrintScan Lakewood for your safety and security needs.",
        "address1": "10455 W 6th Ave #100",
        "address2": None,
        "stateCountry": "CO",
        "city": "Lakewood",
        "postalCode": "80215",
        "county": "Jefferson",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -105.115540,
        "latitude": 39.726331,
        "googlePlaceId": None,
        "referenceId": "62",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "8f086c8c-9411-4ff6-9fe4-f367c9831d34",
        "name": "Business Mail Boutique LLC",
        "displayName": "PrintScan Authorized Fingerprint Service Center- Sugar Land, TX",
        "description": None,
        "metaDescription": "Explore PrintScan in Sugar Land, Texas, your reliable source for professional Live Scan and Fingerprinting services. Benefit from our state-of-the-art technology for accurate and trustworthy results.",
        "notes": "Explore PrintScan in Sugar Land, Texas, your reliable source for professional Live Scan and Fingerprinting services. Benefit from our state-of-the-art technology for accurate and trustworthy results. Located at 11645 S Highway 6.",
        "address1": "11645 S Texas 6",
        "address2": None,
        "stateCountry": "TX",
        "city": "Sugar Land",
        "postalCode": "77498-1302",
        "county": "Fort Bend",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -95.649871,
        "latitude": 29.646417,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 1,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-06:00"
            },
            {
                "dayOfWeek": 2,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-06:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-06:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-06:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2020-01-01T09:00:00-05:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T18:00:00-06:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T11:00:00-06:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-06:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "58f59450-b4bb-4f45-aebd-f43575e2fc70",
        "name": "Kiowa County Public HealtThurs) Public Health (Open Mon-Thur) :\"",
        "displayName": "PrintScan | Kiowa County Public HealtThurs) Public Health (Open Mon-Thur) :\" - Eads, CO",
        "description": "",
        "metaDescription": "Discover PrintScan Eads, Colorado, the trusted provider of high-quality Live Scan and Fingerprinting services. Rely on our secure, swift, and reliable fingerprinting solutions. Experience the PrintScan difference today.",
        "notes": "Discover PrintScan Eads, Colorado, the trusted provider of high-quality Live Scan and Fingerprinting services. Rely on our secure, swift, and reliable fingerprinting solutions. Experience the PrintScan difference today.",
        "address1": "1309 Maine St",
        "address2": None,
        "stateCountry": "CO",
        "city": "Eads",
        "postalCode": "81036",
        "county": "Kiowa",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -102.781445,
        "latitude": 38.479611,
        "googlePlaceId": None,
        "referenceId": "84",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "31fdd2f5-5c87-470b-8a05-f4c070b8ecf4",
        "name": "Montrose County Sheriff’s Office - West End Substation (Open Mon-Thurs)",
        "displayName": "PrintScan | Montrose County Sheriff’s Office - West End Substation (Open Mon-Thurs) - Nucla, CO",
        "description": "Entrance is at the \"Tan Metal Building\"",
        "metaDescription": "Experience top-notch Live Scan and Fingerprinting services at PrintScan Naturita, Colorado. Trust in our secure, efficient, and reliable fingerprinting solutions for all your needs. Choose PrintScan today.",
        "notes": "Experience top-notch Live Scan and Fingerprinting services at PrintScan Naturita, Colorado. Trust in our secure, efficient, and reliable fingerprinting solutions for all your needs. Choose PrintScan today.",
        "address1": "27700 DD Rd",
        "address2": None,
        "stateCountry": "CO",
        "city": "Nucla",
        "postalCode": "81424",
        "county": "Montrose",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -108.562501,
        "latitude": 38.241119,
        "googlePlaceId": None,
        "referenceId": "105",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "b2dc877d-15db-43a8-bf77-f507054e476c",
        "name": "Copy Copy Grand Junction (Open Tues-Thurs)",
        "displayName": "PrintScan | Copy Copy Grand Junction (Open Tues-Thurs) - Grand Junction, CO",
        "description": "",
        "metaDescription": "Experience superior Live Scan and Fingerprinting services at PrintScan Grand Junction, Colorado. Trust in our secure, efficient, and reliable fingerprinting solutions for all your needs. Choose PrintScan today.",
        "notes": "Experience superior Live Scan and Fingerprinting services at PrintScan Grand Junction, Colorado. Trust in our secure, efficient, and reliable fingerprinting solutions for all your needs. Choose PrintScan today.",
        "address1": "401 North Ave",
        "address2": None,
        "stateCountry": "CO",
        "city": "Grand Junction",
        "postalCode": "81501",
        "county": "Mesa",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -108.565798,
        "latitude": 39.077182,
        "googlePlaceId": None,
        "referenceId": "25",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "ff5b064e-5295-4a2e-b065-faee87394a6b",
        "name": "CMB Consultancy LLC",
        "displayName": "PrintScan - Authorized Fingerprint Service Center- Staten Island, NY",
        "description": "Second floor office suites",
        "metaDescription": "Turn to PrintScan in Staten Island, New York for premium Live Scan and Fingerprinting services. We deliver secure, quick, and trustworthy identification solutions tailored to your specific needs.",
        "notes": "Turn to PrintScan in Staten Island, New York for premium Live Scan and Fingerprinting services. We deliver secure, quick, and trustworthy identification solutions tailored to your specific needs.",
        "address1": "1880 Hylan Blvd",
        "address2": "Suite 2R-11",
        "stateCountry": "NY",
        "city": "Staten Island",
        "postalCode": "10305",
        "county": "Richmond",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -74.095288,
        "latitude": 40.583178,
        "googlePlaceId": None,
        "referenceId": None,
        "isActive": True,
        "distance": None,
        "locationHours": [
            {
                "dayOfWeek": 2,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T19:00:00-04:00"
            },
            {
                "dayOfWeek": 3,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T19:00:00-04:00"
            },
            {
                "dayOfWeek": 4,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T19:00:00-04:00"
            },
            {
                "dayOfWeek": 5,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T19:00:00-04:00"
            },
            {
                "dayOfWeek": 6,
                "timeOpen": "2000-01-01T10:00:00-04:00",
                "timeLunch": None,
                "timeResume": None,
                "timeClose": "2000-01-01T15:00:00-04:00"
            }
        ],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "07575bad-30ef-4491-8b8a-fbd18b658ee8",
        "name": "O&M Drug & Alcohol Testing Solutions Greeley (Open Mon-Fri)",
        "displayName": "PrintScan | O&M Drug & Alcohol Testing Solutions Greeley (Open Mon-Fri) - Greeley, CO",
        "description": "Suite C",
        "metaDescription": "Choose PrintScan Greeley, Colorado for premium Live Scan and Fingerprinting services. Enjoy our swift, secure, and reliable fingerprinting solutions tailored to your needs. Experience the PrintScan advantage today.",
        "notes": "Choose PrintScan Greeley, Colorado for premium Live Scan and Fingerprinting services. Enjoy our swift, secure, and reliable fingerprinting solutions tailored to your needs. Experience the PrintScan advantage today.",
        "address1": "1705 1st Ave",
        "address2": None,
        "stateCountry": "CO",
        "city": "Greeley",
        "postalCode": "80631",
        "county": "Weld",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -104.678546,
        "latitude": 40.411472,
        "googlePlaceId": None,
        "referenceId": "111",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    },
    {
        "locationId": "2cd7e779-a859-4b62-8563-fd3b6395c37f",
        "name": "Centro De La Familia (Open Thursday)",
        "displayName": "PrintScan | Centro De La Familia (Open Thursday) - Grand Junction, CO",
        "description": "Suite 111 at the far right end",
        "metaDescription": "Visit PrintScan Grand Junction, Colorado for unparalleled Live Scan and Fingerprinting services. Benefit from our quick, secure, and dependable fingerprinting solutions. Discover the PrintScan commitment to quality today.",
        "notes": "Visit PrintScan Grand Junction, Colorado for unparalleled Live Scan and Fingerprinting services. Benefit from our quick, secure, and dependable fingerprinting solutions. Discover the PrintScan commitment to quality today.",
        "address1": "685 W Gunnison Ave",
        "address2": None,
        "stateCountry": "CO",
        "city": "Grand Junction",
        "postalCode": "81501",
        "county": "Mesa",
        "phone": "806-786-6565",
        "email": "testing@printscan.com",
        "longitude": -108.578056,
        "latitude": 39.072411,
        "googlePlaceId": None,
        "referenceId": "120",
        "isActive": True,
        "distance": None,
        "locationHours": [],
        "appointmentAvailabilityDetails": None,
        "hideSelectButtons": False,
        "index": 0,
        "place": None
    }
]


single_location_detail = {
    "locationId": "abda8dfc-f421-ec11-981f-000d3a12914c",
    "clientId": "90794b96-a750-46c2-b982-189cfc3ef536",
    "name": "PrintScan - Authorized Fingerprint Service Center - Randallstown, MD",
    "client": "Accurate Notary & Fingerprinting",
    "address1": "9830 Liberty Road",
    "address2": None,
    "city": "Randallstown",
    "state": "MD",
    "postalCode": "21133",
    "phone": "806-786-6565",
    "isActive": True,
    "isInOfficeVicinity": False,
    "serviceTypes": [
        "Photograph",
        "SWFT",
        "Live Scan"
    ],
    "isSterlingLocation": False,
    "isPrintScanLocationActive": True,
    "isSterlingLocationActive": False
}

single_location_days = [
    "2024-09-14T00:00:00+00:00",
    "2024-09-16T00:00:00+00:00",
    "2024-09-17T00:00:00+00:00",
    "2024-09-18T00:00:00+00:00",
    "2024-09-19T00:00:00+00:00",
    "2024-09-20T00:00:00+00:00",
    "2024-09-21T00:00:00+00:00",
    "2024-09-23T00:00:00+00:00",
    "2024-09-24T00:00:00+00:00",
    "2024-09-25T00:00:00+00:00",
    "2024-09-26T00:00:00+00:00",
    "2024-09-27T00:00:00+00:00",
    "2024-09-28T00:00:00+00:00",
    "2024-09-30T00:00:00+00:00",
    "2024-10-01T00:00:00+00:00",
    "2024-10-02T00:00:00+00:00",
    "2024-10-03T00:00:00+00:00",
    "2024-10-04T00:00:00+00:00",
    "2024-10-05T00:00:00+00:00"
]


single_location_times = [{
    "startDate": "2024-09-14T12:50:00-04:00",
    "endDate": "2024-09-14T13:00:00-04:00",
    "capacity": 2
}, {
    "startDate": "2024-09-14T13:00:00-04:00",
    "endDate": "2024-09-14T13:10:00-04:00",
    "capacity": 2
}, {
    "startDate": "2024-09-14T13:10:00-04:00",
    "endDate": "2024-09-14T13:20:00-04:00",
    "capacity": 2
}, {
    "startDate": "2024-09-14T13:20:00-04:00",
    "endDate": "2024-09-14T13:30:00-04:00",
    "capacity": 2
}, {
    "startDate": "2024-09-14T13:30:00-04:00",
    "endDate": "2024-09-14T13:40:00-04:00",
    "capacity": 2
}, {
    "startDate": "2024-09-14T13:40:00-04:00",
    "endDate": "2024-09-14T13:50:00-04:00",
    "capacity": 2
}, {
    "startDate": "2024-09-14T13:50:00-04:00",
    "endDate": "2024-09-14T14:00:00-04:00",
    "capacity": 2
}, {
    "startDate": "2024-09-14T14:00:00-04:00",
    "endDate": "2024-09-14T14:10:00-04:00",
    "capacity": 2
}, {
    "startDate": "2024-09-14T14:10:00-04:00",
    "endDate": "2024-09-14T14:20:00-04:00",
    "capacity": 2
}, {
    "startDate": "2024-09-14T14:20:00-04:00",
    "endDate": "2024-09-14T14:30:00-04:00",
    "capacity": 2
}, {
    "startDate": "2024-09-14T14:30:00-04:00",
    "endDate": "2024-09-14T14:40:00-04:00",
    "capacity": 2
}, {
    "startDate": "2024-09-14T14:40:00-04:00",
    "endDate": "2024-09-14T14:50:00-04:00",
    "capacity": 2
}, {
    "startDate": "2024-09-14T14:50:00-04:00",
    "endDate": "2024-09-14T15:00:00-04:00",
    "capacity": 2
}]

class PrintScan:


    def __init__(self,*args, **kwargs) -> None:
        self.header = {
            "Ocp-Apim-Subscription-Key": settings.PRINTSCAN_SUBSCRIPTION_KEY
        }
        self.base_url = 'https://api-printscan.azure-api.net'


    def get_all_locations(self):
        url = f"{self.base_url}/integrator-staging/location"
        response = requests.get(url,headers=self.header)
        if response.ok:
            json_data = response.json()
            new_res = []
            new_res_dict = {}
            for record in json_data:
                stateCountry = record['stateCountry']
                stateCountryName = usa_state_2_code.get(stateCountry)
                if stateCountryName not in new_res_dict:
                    new_res_dict[stateCountryName] = {"stateCountry":stateCountry,"locations":[]}
                    
                new_res_dict[stateCountryName]['locations'].append(
                        dict(
                            locationId=record.get("locationId"),
                            name=record.get("name"),
                            displayName=record.get("displayName"),
                            address1=record.get("address1"),
                            address2=record.get("address2"),
                            longitude=record.get("longitude"),
                            latitude=record.get("latitude"),
                            locationAddress=f"{record.get('address1')}, {record.get('name')}",
                            phone=record.get("phone"),
                            postalCode=record.get("postalCode"),
                            notes=record.get("notes"),
                            city=record.get("city"),
                            county=record.get("county"),
                            place=record.get("place"),
                            distance=record.get("distance"),
                            isActive=record.get("isActive"),
                        )
                    )
                

            for key , value in new_res_dict.items():
                new_res.append(
                    {
                        "stateCountryDisplayName":key,
                        "stateCountryCode":value['stateCountry'],
                        "locations":value['locations']
                    }
                )


                    # new_res.append(
                    #     dict(
                    #         locationId=record.get("locationId"),
                    #         name=record.get("name"),
                    #         displayName=record.get("displayName"),
                    #         isActive=record.get("isActive"),
                    #     )
                    # )
            return new_res
        
        return []

    
    def get_single_location(self,location_id):
        url = f"{self.base_url}/integrator-staging/location/{location_id}"
        response = requests.get(url,headers=self.header)

        if response.ok:
            json_data = response.json()
            return True , json_data
        
        return False , {}


    
    def get_single_single_location_days(self,location_id,application:NationalIdentificationNumberApplication):
        url = f"{self.base_url}/integrator-staging/location/{location_id}/days"
        response = requests.get(url,headers=self.header)
        if response.ok:
            json_data = response.json()
            application.capturing_location_id = location_id
            application.save()
            return json_data
        return []



    def get_single_single_location_times(self,location_id:str,date_string:str):
        url = f"{self.base_url}/integrator-staging/location/{location_id}/times/{date_string}"
        response = requests.get(url,headers=self.header)
        if response.ok:
            json_data = response.json()
            return json_data
        
        return []



    def create_appointment_order(self,location_id,application_ref,appointment_time,**kwargs):
        payload = {
            "clientId": settings.PRINTSCAN_CLIENT_KEY,
            "locationId": location_id,
            "referenceId": application_ref,
            "firstName": kwargs.get("first_name",''),
            "middleName": kwargs.get("middle_name",''),
            "lastName": kwargs.get("last_name",''),
            "email": kwargs.get("email",''),
            "phone": kwargs.get("phone_number",''),
            "appointmentDateTime": appointment_time,
            "appointmentTypeId": "Finra",
            "fingerprint": {
                "recordType": "4"
            }
        }
        print(payload)
        print(settings.PRINTSCAN_CLIENT_KEY)
        url = f"{self.base_url}/integrator-staging/AppointmentOrder"
        print(url)
        response = requests.post(url,headers=self.header,json=payload)
        print(response.text)
        if response.ok:
            return True , response.text

        elif response.status_code == 400:
            # json_data = response.json()
            return False , response.text
        
        return False , response.text




    def submit_appointment_order(self,tracking_id_tcn,tracking_id_tcr,**kwargs):
        payload = {
            "TCN": tracking_id_tcn,
            "TCR": tracking_id_tcr,
            "TOT": "ERRT",
            # "Errors": [{
            #     "Code": "001",
            #     "Message": "Error Message 01"
            # }, {
            #     "Code": "002",
            #     "Message": "Error Message 02"
            # }]
        }
        print(payload)
        url = f"{self.base_url}/integrator-staging/Appointment/Submission"
        print(url)
        response = requests.post(url,headers=self.header,json=payload)
        print(response.text)
        if response.ok:
            return True , response.text

        elif response.status_code == 400:
            # json_data = response.json()
            return False , response.text
        
        return False , response.text


    # 2024-09-16T16:40:00-04:00


# sucess , res = PrintScan().get_single_location(location_id="1982d92b-6ca1-ed11-994d-00224826a175")
# print(res)


# Email.send_capturing_location_detail(
#     email='programmerolakay@gmail.com',
#     name='application_record.first_name', 
#     center_name=res.get('name'),
#     capturing_reference='application_record.capturing_order_ref',
#     city=res.get('city'),
#     state=res.get('state'),
#     address_1=res.get('address1'),
#     address_2=res.get('address2'),
# )