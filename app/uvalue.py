from app import app

"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, render_template, request, session, redirect, url_for, flash
from app import view 
from app import error_handlers 





@app.route('/uvalue', methods=["POST", "GET"])
def u_value():
	if session.get("USERNAME") is not None:
		email = session.get("USERNAME")
		return value()
	else:
		flash("You are not logged in!", 'warning')
		return redirect(url_for("sign_in"))


def value():


    if request.method == "POST":
        L = float(request.form["L"])   # insert cushion thickness
        angle = float(request.form["angle"])   # theta

        import math
        theta = angle * (math.pi/180)
        Tf = 32.5


        ther_exp = 3.2717E-3
        ther_con = 0.026526
        kin_v = 1.6271E-5
        
        ther_dif = 2.2810E-5
        Pr = 0.71332
#import numpy as np
#import matplotlib.pyplot as plt

        while angle == 90:

            Gr = (9.81 * ther_exp * 25 * L ** 3) / kin_v ** 2
            Nu = 0.035 * (Gr * Pr) ** 0.38
            hcv = (Nu * ther_con) / L
            hrd = (4 * 5.67E-8 * Tf ** 4) / 1.35
            R = 1 / (hcv + hrd)
            U = 1 / R
            U = round(U, 2)
            print(" U = for theta = 90")
            print(angle)
            Us = U

            print("U_summer Us at 90")
            print(Us)
            break

        while 0 <= angle <= 67:
            import math
            Gr = (9.81 * ther_exp * 25 * L ** 3) / kin_v ** 2
            Nu = 0.035 * (Gr * Pr) ** 0.38
            Ra = (9.81 * ther_exp * 25 * L ** 3) / (ther_dif * kin_v)
            Nu1 = 0.069 * Ra ** (0.333) * Pr ** 0.074
            Nuf = Nu1 * ((Nu / Nu1) ** (angle / 67)) * ((math.sin(67 * math.pi/180)) ** (angle / 268))
            hcv = (Nuf * ther_con) / L
            hrd = (4 * 5.67E-8 * Tf ** 4) / 1.35
            R = (1 / (hcv + hrd))
            U = 1 /R
            U = round(U, 2)



            print(" U for 67 => theta => 0")
            print(U)
            import math
            Gr = (9.81 * ther_exp * 25 * L ** 3) / kin_v ** 2
            Nu = 1 + ((0.035 * (Gr * Pr) ** 0.38) - 1) * math.sin(theta+(((math.pi/2) - theta) * 2))
            hcv = (Nu * ther_con) / L
            hrd = (4 * 5.67E-8 * Tf ** 4) / 1.35
            R = (1 / (hrd + hcv))
            Us = 1 / R
            Us = round(Us, 2)
            print("Us summer 0 <= theta <= 67")
            print(Us)
            print(angle)
            break

        while 67 < angle < 90:
            Gr = (9.81 * ther_exp * 25 * L ** 3) / kin_v ** 2

            Nu = (0.035 * (Gr * Pr) ** 0.38) * (math.sin(theta)) ** 0.25
            hcv = (Nu * ther_con) / L
            hrd = (4 * 5.67E-8 * Tf ** 4) / 1.35
            R = (1 / (hcv + hrd))
            U = 1 / R
            U = round(U, 2)

            print("U 67 < theta < 90")
            print(U)

            Gr = (9.81 * ther_exp * 25 * L ** 3) / kin_v ** 2
            Nu = 1 + ((0.035 * (Gr * Pr) ** 0.38) - 1) * math.sin(theta+(((math.pi/2) - theta) * 2))
            hcv = (Nu * ther_con) / L
            hrd = (4 * 5.67E-8 * Tf ** 4) / 1.35
            R = (1 / (hrd + hcv))
            Us = 1 / R
            Us = round(Us, 2)
            print(angle)

            print("Us summer 67 < theta < 90")
            print(Us)
            break

        while 90 < angle <= 180:

            Gr = (9.81 * ther_exp * 25 * L ** 3) / kin_v ** 2
            Nu = 1 + ((0.035 * (Gr * Pr) ** 0.38) - 1) * math.sin(theta)
            hcv = (Nu * ther_con) / L
            hrd = (4 * 5.67E-8 * Tf ** 4) / 1.35
            R = (1/(hrd + hcv))
            U = 1 / R
            U = round(U, 2)


            print("U 90 < theta <= 180")
            print(U)

            Gr = (9.81 * ther_exp * 25 * L ** 3) / kin_v ** 2
            import math
            Nu = (0.035 * (Gr * Pr) ** 0.38) * math.sin(theta-((theta-(math.pi/2)) * 2)) ** 0.25
            hcv = (Nu * ther_con) / L
            hrd = (4 * 5.67E-8 * Tf ** 4) / 1.35
            R = (1 / (hcv + hrd))
            Us = 1 / R
            Us = round(Us, 2)
            print("Us for 90 > theta <= 180")
            print(Us)
            break

        return render_template("admin/uvalue_output.html", U=U, Us=Us, L=L, angle=angle)
    return render_template("admin/uvalue_input.html")


