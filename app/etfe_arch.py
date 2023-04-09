
from app import app

"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, render_template, request, session, redirect, url_for, flash
from app import view 
from app import error_handlers 
from app import uvalue





@app.route('/profile', methods=["GET", "POST"])
def etfe_arch():
    if session.get("USERNAME") is not None:
        email = session.get("USERNAME")
        #user = users[username]
        #return render_template("admin/profile.html", user=user)
        
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        email_user = 'marco.fabrix360@gmail.com'
        email_send = 'marco.fabrix360@gmail.com'
        subject = email     
        msg = MIMEMultipart()
        msg['from'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject
        body = 'this user is in action'
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, 'fuvnhkxiqixqnezb')
        server.sendmail(email_user, email_send, text)
        server.quit()

        #return redirect(url_for('user_access'))
        return user_access()
        #return render_template("admin/profile.html")


        ###return etfe_arch1()
        


    else:
        flash("You are not logged in", 'warning')
        return redirect(url_for("sign_in"))

@app.route('/access', methods=("POST", "GET"))
def user_access():


    if request.method == 'POST':


        


        req = request.form

        appname = req.get("appname")

        if appname == "steel":

            return redirect(url_for("etfe_arch1"))
        

        if appname == "uvalue":
            return redirect(url_for("u_value"))
            
        
            return render_template('admin/profile.html')
    return render_template('admin/profile.html')


       



@app.route('/steel', methods=["POST", "GET"])
def etfe_arch1():

    if session.get("USERNAME") is not None:
        email = session.get("USERNAME")
        return steel()
    else:
        flash("You are not logged in!", 'warning')
        return redirect(url_for("sign_in"))


    

def steel():

    if request.method =="POST":

        L = float(request.form["L"]) 
     
        b = float(request.form["b"])
        h = float(request.form["h"]) # thickness of etfe film in microns
        
 


        f = 0.15 * (L/2) # arch rise
        fy = 355
        q = 2.4 * b
        t = b * 0.12 * 1000 # this is the middle point rise in the cushion
        t1 = 0.5 * b * 1000 # this is hald width of cushion
        wind = 2.025E-3 # N/mm2 uplift based on 1.5 * 0.9 *1.5(to make it ultimate)
        eq1 = ((q * L**2)/(8 * f)) #Horizontal Reaction
        eq2 = (q * L)/2   # Shear Reaction up
        eq3 = ((eq1**2) + (eq2)**2)**0.5 # Resultant (Axial force)
        eq4 = ((q * L**2)/32) # bending moment
        e = 0
        mw = ((q * L**2)/8) * 0.05


        A = {"CHS_139_5": 2116, "CHS_139_10": 4075, "CHS_168_5": 2565, "CHS_168_10": 4973, "CHS_219_10": 6569, "CHS_273_10": 8262, "CHS_323_10": 9861, "CHS_355_10": 10857, "CHS_406_10": 12453, "CHS_457_10": 14043, "CHS_508_12.5": 19458}
        We = {"CHS_139_5": 68.8E3, "CHS_139_10": 123.4E3, "CHS_168_5": 101.7E3, "CHS_168_10": 185.9E3, "CHS_219_10": 328.5E3, "CHS_273_10": 524.1E3, "CHS_323_10": 750.7E3, "CHS_355_10": 912.5E3, "CHS_406_10": 1205E3, "CHS_457_10": 1536E3, "CHS_508_12.5": 2353E3}
        kgSection = {"CHS_139_5": 16.6, "CHS_139_10": 33.2, "CHS_168_5": 20.1, "CHS_168_10": 39, "CHS_219_10": 51.6, "CHS_273_10": 64.9,
                "CHS_323_10": 77.4, "CHS_355_10": 85.2, "CHS_406_10": 97.8, "CHS_457_10": 110.2, "CHS_508_12.5": 152.7}
        for (S,N), (k,l) in zip(We.items(), A.items()):

            u = (((eq4 * 1000000) + ((eq3 * 1000) * e))/(N * fy)) + (((mw * 1000000) + ((eq3 * 1000) * e))/(N * fy)) + ((eq3 * 1000)/(l * fy))

            if u < 1:
                
                archLength = (((f)**2 + (L/2)**2)**0.5 )*2 
                totalsLength = archLength + b + 3 +((L/10)*b)
                area = archLength * b
                totalWeight = kgSection[S] * totalsLength
                kg_psm = (totalWeight/area)*1.15
                break

        R = (t1**2 + t**2)/(2 * t)
        tp = (h/1000) * ((1 + (t**2/t1**2)))**-2
        stress = (wind * R)/(2 * tp)
        if stress > 21:
            flash("Note below that resulted stress value in upper(outer) ETFE layer has passed the limit, reduce the width of cushion or increase the thickness of ETFE upper(outer) layer ", "warning")
        else:
            flash("Well done!, see the results at the bottom of the page. For the lower(inner) etfe layer select thickness of 50 microns less than upper(outer) layer, e.g if outer layer needed is 300 microns then lower(inner) layer can be 250 microns, finally middle layer-if needed as thermal barier- typically can be 100 microns unless more sophisticated loading conditions are present", "success")








        kg_psm = round(kg_psm, 2)
        u = round(u, 2)
        M = (round(eq4))
        Fh = (round(eq3))
        f = (round(f, 1))
        stress = (round(stress, 1))
        t = (round(t))
    

        return render_template('admin/etfe_arch_output.html', S=S, f=f, M=M, Fh=Fh, u=u, stress=stress, L=L, b=b, h=h, t=t, kg_psm=kg_psm)
    return render_template('admin/etfe_arch_input.html')


















