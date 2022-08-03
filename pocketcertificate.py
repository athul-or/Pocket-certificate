import datetime
from flask import Flask, render_template, request, redirect, session, send_file
import random
from DBConnection import Db
from asw_img_encr import IMG_xor

app = Flask(__name__)
app.secret_key="abc"
# rule


@app.route('/logout')
def logout():
    session['lo']=""
    # session.clear()
    return redirect('/login')

@app.route('/')
def user_homepage():
    return render_template("index_home.html")




@app.route('/login', methods=['get', 'post'])
def login():
    if request.method == 'POST':
        username = request.form['textfield']
        password = request.form['textfield2']
        # print(username, password)
        db = Db()
        query = db.selectOne("select * from login where username='" + username + "' and password='" + password + "'")
        if query is not None:
            session['lid'] = query['login_id']
            session['lo']="li"
            if query['usertype'] == 'admin':
                session['aemail']=query['username']
                return redirect('/admin_home')
            elif query['usertype']=='VILLAGE_OFFICER':
                a=db.selectOne("select * from village where login_id='"+str(session['lid'])+"'")
                session['v_name']=a['v_name']
                session['v_email']=a['v_email']
                session['v_image'] = a['v_image']
                return redirect('/village_home')
            elif query['usertype']=='CLERK':
                session['lid']=query['login_id']
                a = db.selectOne("select * from clerk where login_id='" + str(session['lid']) + "'")
                session['c_name'] = a['c_name']
                session['c_email'] = a['c_email']
                session['c_image'] = a['c_image']
                return redirect('/clerk_home')
            elif query['usertype']=='USER':
                a = db.selectOne("select * from user where user_id='" + str(session['lid']) + "'")
                session['u_name'] = a['u_name']
                session['u_email'] = a['email']
                session['u_image'] = a['image']
                return redirect('/user_home')
            else:
                return '''<script>alert('not found');window.location="/"</script>'''
        else:
            return '''<script>alert('not found');window.location="/"</script>'''
    else:
        return render_template('login.html')


@app.route('/admin_home')
def admin_home():
    if session['lo']=="li":
        return render_template('admin/index.html')
    else:
        return redirect('/login')

@app.route('/add_dept',methods=['GET','POST'])
def add_dept_action():
    if session['lo'] == "li":
        if request.method=='POST':
            dept_name=request.form['textfield3']
            certificate_name=request.form['textfield2']
            dept_details=request.form['textfield4']
            proof_id=request.form.getlist('CheckboxGroup1')
            ss=(',').join(proof_id)
            db = Db()
            query = db.insert("insert into department_add values('','"+dept_name+"','"+certificate_name+"','"+dept_details+"','"+str(ss)+"')")
            return '''<script>alert("Department Added");window.location="/admin_home"</script>'''
        else:
            return render_template('admin/add_dept.html')
    else:
        return redirect('/login')

@app.route('/view_dept')
def view_dept():
     if session['lo'] == "li":
        db=Db()
        a=db.select("select * from department_add")
        return render_template('admin/view_dept.html',data=a)
     else:
         return redirect('/login')

@app.route('/edit_dept/<b>',methods=['GET','POST'])
def edit_dept(b):
    if session['lo'] == "li":
        db=Db()
        if request.method=='POST':
            dept_name = request.form['textfield3']
            certificate_name = request.form['textfield2']
            d_details = request.form['textfield4']
            proof_id = request.form.getlist('CheckboxGroup1')
            ss = (',').join(proof_id)
            db.update("update department_add set dept_name='"+dept_name+"',certificate_name='"+certificate_name+"',d_details='"+d_details+"',proof_id='"+str(ss)+"'where dept_id='"+b+"'")
            return view_dept()



        a=db.selectOne("select * from department_add where dept_id='"+b+"'")
        pid=a['proof_id']
        pidd=pid.split(',')
        print(pidd)
        return render_template('admin/edit_dept.html',data=a,d1=pidd)
    else:
        return redirect('/login')

@app.route('/delete_dept/<c>')
def delete_dept(c):
    if session['lo'] == "li":
        db=Db()
        a=db.delete("delete from department_add where dept_id='"+c+"'")
        return redirect('/view_dept')
    else:
        return redirect('/login')


@app.route('/add_village',methods=['get','post'])
def add_village():
    if session['lo'] == "li":
        if request.method=='POST':
            name=request.form['textfield']
            place=request.form['textfield10']
            district=request.form['textfield9']
            pin=request.form['textfield2']
            post=request.form['textfield8']
            image=request.files['fileField']
            email=request.form['textfield15']
            date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            image.save(r"C:\Users\Athul\PycharmProjects\pocketcertificate\static\image\\"+date+".jpg")
            path=("/static/image//"+date+".jpg")
            qualification=request.form['textfield7']
            phoneno=request.form['textfield3']
            joiningdate=request.form['textfield4']
            enddate=request.form['textfield5']
            password=random.randint(0000,9999)
            db = Db()
            qry=db.insert("insert into login VALUES ('','"+email+"','"+str(password)+"','VILLAGE_OFFICER')")
            db.insert("insert into village values('"+str(qry)+"','"+name+"','"+place+"','"+post+"','"+pin+"','"+district+"','"+str(path)+"','"+qualification+"','"+email+"','"+joiningdate+"','"+enddate+"','"+phoneno+"')")
            return '''<script>alert('successfull');window.location="/admin_home"</script>'''
        else:
             return render_template('admin/edit_vilage.html')
    else:
        return redirect('/login')

@app.route('/view_village')
def view_village():
    if session['lo'] == "li":
         db=Db()
         b=db.select("select * from village")
         return render_template('admin/view_village.html',data=b)
    else:
        return redirect('/login')

@app.route('/update_village/<d>',methods=['POST','GET'])
def edit_village(d):
    if session['lo'] == "li":
        db=Db()
        if request.method=="POST":
            name = request.form['textfield']
            place = request.form['textfield10']
            district = request.form['textfield9']
            pin = request.form['textfield2']
            post = request.form['textfield8']
            image = request.files['fileField']
            date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            image.save(r"C:\Users\Athul\PycharmProjects\pocketcertificate\static\image\\" + date + ".jpg")
            path = ("/static/image/" + date + ".jpg")
            qualification = request.form['textfield7']
            phoneno = request.form['textfield3']
            joiningdate = request.form['textfield4']
            enddate = request.form['textfield5']
            if request.files != None:
                if image.filename != "":
                    db.update( "update village set v_name='" + name + "',v_place='" + place + "',v_pin='" + pin + "',v_post='" + post + "',v_district='" + district + "',v_image='" + str(path) + "',v_qualification='" + qualification + "',joining_date='" + joiningdate + "',end_date='" + enddate + "',v_phone='" + phoneno +"'where login_id='"+ d+ "'")
                    return '''<script>alert("success");window.location="/view_village"</script>'''
                else:
                    db.update("update village set v_name='" + name + "',v_place='" + place + "',v_pin='" + pin + "',v_post='" + post + "',v_district='" + district + "',v_qualification='" + qualification + "',joining_date='" + joiningdate + "',end_date='" + enddate + "',v_phone='"+phoneno+"' where login_id='" + d + "'")
                    return '''<script>alert("success");window.location="/view_village"</script>'''
            else:
                db.update("update village set v_name='" + name + "',v_place='" + place + "',v_pin='" + pin + "',v_post='" + post + "',v_district='" + district + "',v_qualification='" + qualification + "',joining_date='" + joiningdate + "',end_date='" + enddate + "',v_phone='"+phoneno+"'where login_id='"+d+"'")
                return '''<script>alert("success");window.location="/view_village"</script>'''

        a=db.selectOne("select * from village where login_id='"+d+"'")

        return render_template('admin/update_village.html',data=a)
    else:
        return redirect('/login')

@app.route('/delete_village/<e>')
def delete_village(e):
    if session['lo'] == "li":
        db=Db()
        a=db.delete("delete from village where login_id='"+e+"'")
        a1=db.delete("delete from login where login_id='"+e+"'")
        return redirect('/view_village')
    else:
        return redirect('/login')

@app.route('/add_clerk/<v>',methods=['GET','POST'])
def add_clerk(v):
    if session['lo'] == "li":
        if request.method=='POST':
            name = request.form['textfield']
            place = request.form['textfield10']
            district = request.form['select']
            pin = request.form['textfield2']
            post = request.form['textfield8']
            image = request.files['fileField']
            email = request.form['textfield6']
            date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            image.save(r"C:\Users\Athul\PycharmProjects\pocketcertificate\static\image\\" + date + ".jpg")
            path = ("/static/image/" + date + ".jpg")
            qualification = request.form['textfield7']
            phoneno = request.form['textfield3']
            joiningdate = request.form['textfield4']
            enddate = request.form['textfield5']
            password = random.randint(0000, 9999)
            db = Db()
            qry = db.insert("insert into login VALUES ('','" + email + "','" + str(password) + "','CLERK')")
            db.insert("insert into clerk values('" + str(qry) + "','" + name + "','" + place + "','" + pin + "','" + post + "','" + district + "','" + str(path) + "','" + qualification + "','" + email + "','" + joiningdate + "','" + enddate + "','" + phoneno + "','"+str(v)+"')")
            return '''<script>alert('successfull');window.location="/admin_home"</script>'''
        else:
            return render_template('admin/clerk.html')
    else:
        return redirect('/login')

@app.route('/view_clerk')
def view_clerk():
    if session['lo'] == "li":
        db = Db()
        b = db.select("select * from clerk,department_add where clerk.d_id=department_add.dept_id")
        return render_template('admin/view_clerk.html',data=b)
    else:
        return redirect('/login')


@app.route('/upclrk/<cid>')
def upclrk(cid):
    if session['lo'] == "li":
        db=Db()
        qry=db.selectOne("select * from clerk where login_id='"+cid+"'")
        return render_template('admin/edit_clerk.html', loop1=qry,id=cid)
    else:
        return redirect('/login')


@app.route('/upclrk1/<cid>',methods=['post'])
def upclrk1(cid):
    if session['lo'] == "li":
        db=Db()
        name = request.form['textfield']
        place = request.form['textfield10']
        district = request.form['select']
        pin = request.form['textfield2']
        post = request.form['textfield8']
        image = request.files['fileField']
        date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        image.save(r"C:\Users\Athul\PycharmProjects\pocketcertificate\static\image\\" + date + ".jpg")
        path = ("/static/image//" + date + ".jpg")
        qualification = request.form['textfield7']
        phoneno = request.form['textfield3']
        joiningdate = request.form['textfield4']
        enddate = request.form['textfield5']
        did = request.form['textfield20']
        if request.files!=None:
            if image.filename!="":
                db.update("update clerk set c_name='" + name + "',c_place='" + place + "',c_pin='" + pin + "',c_post='" + post + "',c_district='" + district + "',c_image='" + str(path) + "',c_qualification='" + qualification + "',cjoining_date='" + joiningdate + "',cending_date='" + enddate + "',c_phone='" + phoneno + "',d_id='" + did + "'where login_id='" + cid + "'")
                return '''<script>alert("success");window.location="/view_clerk"</script>'''
            else:
                db.update("update clerk set c_name='" + name + "',c_place='" + place + "',c_pin='" + pin + "',c_post='" + post + "',c_district='" + district + "',c_qualification='" + qualification + "',cjoining_date='" + joiningdate + "',cending_date='" + enddate + "',c_phone='" + phoneno + "',d_id='" + did + "'where login_id='" + cid + "'")
                return '''<script>alert("success");window.location="/view_clerk"</script>'''
        else:
            db.update( "update clerk set c_name='" + name + "',c_place='" + place + "',c_pin='" + pin + "',c_post='" + post + "',c_district='" + district + "',c_qualification='" + qualification + "',cjoining_date='" + joiningdate + "',cending_date='" + enddate + "',c_phone='" + phoneno + "',d_id='" + did + "'where login_id='" + cid + "'")
            return '''<script>alert("success");window.location="/view_clerk"</script>'''
    else:
        return redirect('/login')



@app.route('/delete_clerk/<g>')
def delete_clerk(g):
    if session['lo'] == "li":
        db=Db()
        a=db.delete("delete from clerk where login_id='"+g+"'")
        a1 = db.delete("delete from login where login_id='" + g + "'")
        return redirect('/view_clerk')
    else:
        return redirect('/login')



@app.route('/view_feedback')
def view_feedback():
    if session['lo'] == "li":
        db = Db()
        b = db.select("select * from feedback,user where feedback.fuser_id=user.user_id")
        return render_template('admin/view_feedback.html', data=b)
    else:
        return redirect('/login')


@app.route('/view_complaint')
def complaint():
    if session['lo'] == "li":
        db = Db()
        b = db.select("select * from complaint,user where reply='pending' and user.user_id=complaint.userid")
        return render_template('admin/view_complaint.html', data=b)
    else:
        return redirect('/login')

@app.route('/notification_send',methods=['GET','POST'])
def noti():
    if session['lo'] == "li":
        if request.method=='POST':
            notification=request.form['textarea']
            db=Db()
            q=db.insert("insert into notification VALUES ('','"+notification+"',curdate()) ")
            return  '''<script>alert("notification send");window.location="/admin_home"</script>'''
        else:
            return render_template('admin/notification.html')
    else:
        return redirect('/login')

@app.route('/complaint_reply/<k>',methods=['GET','POST'])
def reply(k):
    if session['lo'] == "li":
        if request.method=='POST':
            reply=request.form['textarea']
            db=Db()
            db.update("update complaint set reply='"+reply+"',reply_date=curdate() where complaint_id='"+str(k)+"'")
            return '''<script>alert("Reply send");window.location="/admin_home"</script>'''
        else:
            return render_template('admin/complaint _reply.html')
    else:
        return redirect('/login')



















#Second Module

@app.route('/view_profile',methods=['GET','POST'])
def profile():
    if session['lo'] == "li":
        db=Db()
        ss=db.selectOne("select * from village WHERE login_id='"+str(session['lid'])+"'")
        print(ss)
        return  render_template("village officer/view_profile.html",data=ss)
    else:
        return redirect('/login')


@app.route('/village_home')
def village_home():
    if session['lo'] == "li":
        return render_template('village officer/village_home.html')
    else:
        return redirect('/login')


@app.route('/view_department')
def view_department():
    if session['lo'] == "li":
        db=Db()
        a=db.select("select * from department_add")
        return render_template('village officer/view_department.html',data=a)
    else:
        return redirect('/login')

@app.route('/view_village_clerk')
def view_village_clerk():
    if session['lo'] == "li":
        db = Db()
        b = db.select("select * from clerk,department_add where clerk.d_id=department_add.dept_id")
        print(b)
        return render_template('village officer/view_clerk.html',data=b)
    else:
        return redirect('/login')

@app.route('/application_request')
def application_request():
    if session['lo'] == "li":
        return render_template('village officer/request.html')
    else:
        return redirect('/login')

@app.route('/vview_proof/<uid>')
def vview_proof(uid):
    if session['lo'] == "li":
        db=Db()
        q=db.select("select * from certificate where userid='"+uid+"'")
        return render_template('village officer/view_proof.html',data=q)
    else:
        return redirect('/login')

@app.route("/clerk_download_proof/<cert_id>")
def clerk_download_proof(cert_id):
    db=Db()
    res=db.selectOne("select certificate from certificate where certificate_id='"+cert_id+"'")
    res2=db.selectOne("select * from xor_keys where certificate_id='"+cert_id+"'")
    obj = IMG_xor()
    path=str(res['certificate']).split("/")[-1]
    pth = obj.dec(path, res2['key1'], res2['key2'], res2['key3'])
    return send_file("C:\\Users\\Athul\\PycharmProjects\\pocketcertificate\\static\\decrypted\\" + pth, as_attachment=True)


@app.route('/income_request')
def income_request():
    if session['lo'] == "li":
        db=Db()
        res=db.select("select * from income,user WHERE income.inc_userid=user.user_id and income.status='Forwarded'")
        return render_template('village officer/income_request.html',data=res)
    else:
        return redirect('/login')

@app.route('/income_approve/<id>')
def income_approve(id):
    if session['lo'] == "li":
        db=Db()
        db.update("update income set status='Approved' WHERE inc_id='"+id+"'")
        return '''<script>alert("Approved");window.location="/income_request"</script>'''
    else:
        return redirect('/login')

@app.route('/income_reject/<id>')
def income_reject(id):
    if session['lo'] == "li":
        db=Db()
        db.update("update income set status='Rejected' WHERE inc_id='"+id+"'")
        return '''<script>alert("Rejected");window.location="/income_request"</script>'''
    else:
        return redirect('/login')

@app.route('/marriage_request')
def marriage_request():
    if session['lo'] == "li":
        db=Db()
        a=db.select("select w.u_name as wn,w.dob as wdob ,w.district as wd,w.taluk as wt,w.village as wv ,h.u_name as hn,h.dob as hdob ,h.district as hd,h.taluk as ht,h.village as hv,marriage.* from marriage,user as w,user as h where marriage.wmcuserid=w.user_id and marriage.hmcuserid=h.user_id and marriage.status='Forwarded'")
        return render_template('village officer/marriage_request.html',data=a)
    else:
        return redirect('/login')


@app.route('/marriage_approve/<id>')
def marriage_approve(id):
    if session['lo'] == "li":
        db=Db()
        db.update("update marriage set status='Approved' WHERE mcid='"+id+"'")
        return '''<script>alert("Approved");window.location="/marriage_request"</script>'''
    else:
        return redirect('/login')


@app.route('/marriage_reject/<id>')
def marriage_reject(id):
    if session['lo'] == "li":
        db=Db()
        db.update("update marriage set status='Rejected' WHERE mcid='"+id+"'")
        return '''<script>alert("Rejected");window.location="/marriage_request"</script>'''
    else:
        return redirect('/login')


@app.route('/caste_request')
def caste_request():
    if session['lo'] == "li":
        db = Db()
        b=db.select("select * from caste,user WHERE caste.cuserid=user.user_id and caste.status='Forwarded'")
        return render_template('village officer/caste_request.html',data=b)
    else:
        return redirect('/login')


@app.route('/caste_approve/<id>')
def caste_approve(id):
    if session['lo'] == "li":
        db=Db()
        db.update("update caste set status='Approved' WHERE ccid='"+id+"'")
        return '''<script>alert("Approved");window.location="/caste_request"</script>'''
    else:
        return redirect('/login')


@app.route('/caste_reject/<id>')
def caste_reject(id):
    if session['lo'] == "li":
        db=Db()
        db.update("update caste set status='Rejected' WHERE ccid='"+id+"'")
        return '''<script>alert("Rejected");window.location="/caste_request"</script>'''
    else:
        return redirect('/login')


@app.route('/nativity_request')
def nativity_request():
    if session['lo'] == "li":
        db=Db()
        a = db.select("select f.u_name,f.phoneno,f.email,f.housename,f.place,f.district,f.post,f.pin,f.father_name as fn,f_district as fd,f_taluk as ft,f_village as fv ,f.mother_name as mn,m_district as md,m_taluk as mt,m_village as mv,nativity.* from nativity,user as f,user as m where nativity.ncuserid=f.user_id and nativity.ncuserid=m.user_id and nativity.status='Forwarded'")
        return render_template('village officer/nativity_request.html',data=a)
    else:
        return redirect('/login')


@app.route('/nativity_approve/<id>')
def nativity_approve(id):
    if session['lo'] == "li":
        db=Db()
        db.update("update nativity set status='Approved' WHERE ncid='"+id+"'")
        return '''<script>alert("Approved");window.location="/nativity_request"</script>'''
    else:
        return redirect('/login')


@app.route('/nativity_reject/<id>')
def nativity_reject(id):
    if session['lo'] == "li":

        db=Db()
        db.update("update nativity set status='Rejected' WHERE ncid='"+id+"'")
        return '''<script>alert("Rejected");window.location="/nativity_request"</script>'''
    else:
        return redirect('/login')


@app.route('/view_approved_application')
def view_approved_application():
    if session['lo'] == "li":
        return render_template('village officer/APPROVED.html')
    else:
        return redirect('/login')

@app.route('/approved_nativity_application')
def approved_nativity_application():
    if session['lo'] == "li":
        db = Db()
        b = db.select("SELECT * FROM NATIVITY,USER WHERE NATIVITY.ncuserid=user.user_id")
        print(b)
        return render_template('village officer/view approved nativity.html',data=b)
    else:
        return redirect('/login')

@app.route('/approved_marriage_application')
def approved_marriage_application():
    if session['lo'] == "li":
        db = Db()
        b = db.select("select w.u_name as wn,w.dob as wdob ,w.district as wd,w.taluk as wt,w.village as wv ,h.u_name as hn,h.dob as hdob ,h.district as hd,h.taluk as ht,h.village as hv,marriage.* from marriage,user as w,user as h where marriage.wmcuserid=w.user_id and marriage.hmcuserid=h.user_id")
        print(b)
        return render_template('village officer/view approved marriage.html',data=b)
    else:
        return redirect('/login')

@app.route('/approved_caste_application')
def approved_caste_application():
    if session['lo'] == "li":
        db = Db()
        b = db.select("select * from caste,user WHERE caste.cuserid=user.user_id")
        return render_template('village officer/view_approved_caste.html',data=b)
    else:
        return redirect('/login')



@app.route('/approved_income_application')
def approved_income_application():
    if session['lo'] == "li":
        db = Db()
        b = db.select("select * from income,user WHERE income.inc_userid=user.user_id")
        return render_template('village officer/view_approved_income.html',data=b)
    else:
        return redirect('/login')


@app.route('/view_notification')
def view_notification():
    if session['lo'] == "li":
        db = Db()
        b = db.select("select * from notification")
        return render_template('village officer/view_notification.html',data=b)
    else:
        return redirect('/login')


















#THIRD MODULE

@app.route('/clerk_home')
def clerk_home():
    if session['lo'] == "li":
        return render_template('clerk/clerk_home.html')
    else:
        return redirect('/login')


@app.route('/certificate_category')
def certificate_category():
    if session['lo'] == "li":
        db=Db()
        a=db.select("select * from department_add")
        return render_template('clerk/category.html',data=a)
    else:
        return redirect('/login')


@app.route('/clerk_request')
def clerk_request():
    if session['lo'] == "li":
        return render_template('clerk/clerk_request.html')
    else:
        return redirect('/login')


@app.route('/view_proof/<uid>')
def view_proof(uid):
    if session['lo'] == "li":
        db=Db()
        q=db.select("select * from certificate where userid='"+uid+"'")
        return render_template('clerk/view_proof.html',data=q)
    else:
        return redirect('/login')




@app.route('/clerk_income_request')
def clerk_income_request():
    if session['lo'] == "li":
        db=Db()
        res=db.select("select * from income,user WHERE income.inc_userid=user.user_id and income.status='pending'")
        return render_template('clerk/clerk_income_request.html',data=res)
    else:
        return redirect('/login')



@app.route('/clerk_income_approve/<id>')
def clerk_income_approve(id):
    if session['lo'] == "li":
        db=Db()
        db.update("update income set status='Forwarded' WHERE inc_id='"+id+"'")
        return '''<script>alert("Forwarded");window.location="/clerk_income_request"</script>'''
    else:
        return redirect('/login')


@app.route('/clerk_income_reject/<id>')
def clerk_income_reject(id):
    if session['lo'] == "li":

        db=Db()
        db.update("update income set status='Rejected' WHERE inc_id='"+id+"'")
        return '''<script>alert("Rejected");window.location="/clerk_income_request"</script>'''
    else:
        return redirect('/login')

@app.route('/clerk_marriage_request')
def clerk_marriage_request():
    if session['lo'] == "li":
        db=Db()
        a=db.select("select w.u_name as wn,w.dob as wdob ,w.district as wd,w.taluk as wt,w.village as wv ,h.u_name as hn,h.dob as hdob ,h.district as hd,h.taluk as ht,h.village as hv,marriage.* from marriage,user as w,user as h where marriage.wmcuserid=w.user_id and marriage.hmcuserid=h.user_id and marriage.status='pending'")
        return render_template('clerk/clerk_marriage_request.html',data=a)
    else:
        return redirect('/login')

@app.route('/clerk_marriage_approve/<id>')
def clerk_marriage_approve(id):
    if session['lo'] == "li":

        db=Db()
        db.update("update marriage set status='Forwarded' WHERE mcid='"+id+"'")
        return '''<script>alert("Forwarded");window.location="/clerk_marriage_request"</script>'''
    else:
        return redirect('/login')


@app.route('/clerk_marriage_reject/<id>')
def clerk_marriage_reject(id):
    if session['lo'] == "li":

        db=Db()
        db.update("update marriage set status='Rejected' WHERE mcid='"+id+"'")
        return '''<script>alert("Rejected");window.location="/clerk_marriage_request"</script>'''
    else:
        return redirect('/login')

@app.route('/clerk_caste_request')
def clerk_caste_request():
    if session['lo'] == "li":
        db = Db()
        b=db.select("select * from caste,user WHERE caste.cuserid=user.user_id and caste.status='pending'")
        return render_template('clerk/clerk_caste_request.html',data=b)
    else:
        return redirect('/login')


@app.route('/clerk_caste_approve/<id>')
def clerk_caste_approve(id):
    if session['lo'] == "li":
        db=Db()
        db.update("update caste set status='Forwarded' WHERE ccid='"+id+"'")
        return '''<script>alert("Forwarded");window.location="/clerk_caste_request"</script>'''
    else:
        return redirect('/login')


@app.route('/clerk_caste_reject/<id>')
def clerk_caste_reject(id):
    if session['lo'] == "li":
        db=Db()
        db.update("update caste set status='Rejected' WHERE ccid='"+id+"'")
        return '''<script>alert("Rejected");window.location="/clerk_caste_request"</script>'''
    else:
        return redirect('/login')



@app.route('/clerk_nativity_request')
def clerk_nativity_request():
    if session['lo'] == "li":

        db=Db()
        a = db.select("select nativity.*, f.u_name,f.phoneno,f.email,f.housename,f.place,f.district,f.post,f.pin,f.father_name as fn,f_district as fd,f_taluk as ft,f_village as fv ,f.mother_name as mn,m_district as md,m_taluk as mt,m_village as mv,nativity.* from nativity,user as f,user as m where nativity.ncuserid=f.user_id and nativity.ncuserid=m.user_id and nativity.status='pending'")
        return render_template('clerk/clerk_nativity_request.html',data=a)
    else:
        return redirect('/login')


@app.route('/clerk_nativity_approve/<id>')
def clerk_nativity_approve(id):
    if session['lo'] == "li":

        db=Db()
        db.update("update nativity set status='Forwarded' WHERE ncid='"+id+"'")
        return '''<script>alert("Forwarded");window.location="/clerk_nativity_request"</script>'''
    else:
        return redirect('/login')


@app.route('/clerk_nativity_reject/<id>')
def clerk_nativity_reject(id):
    if session['lo'] == "li":

        db=Db()
        db.update("update nativity set status='Rejected' WHERE ncid='"+id+"'")
        return '''<script>alert("Rejected");window.location="/clerk_nativity_request"</script>'''
    else:
        return redirect('/login')


@app.route('/clerk_application_status')
def clerk_application_status():
    if session['lo'] == "li":

        return render_template('clerk/clerk_application_status.html')
    else:
        return redirect('/login')


@app.route('/clerk_nativity_status')
def clerk_nativity_status():
    if session['lo'] == "li":
        db = Db()
        b = db.select("SELECT * FROM NATIVITY,USER WHERE NATIVITY.ncuserid=user.user_id")
        print(b)
        return render_template('clerk/clerk_nativity_status.html',data=b)
    else:
        return redirect('/login')


@app.route('/clerk_marriage_status')
def clerk_marriage_status():
    if session['lo'] == "li":

        db = Db()
        b = db.select("select w.u_name as wn,w.dob as wdob ,w.district as wd,w.taluk as wt,w.village as wv ,h.u_name as hn,h.dob as hdob ,h.district as hd,h.taluk as ht,h.village as hv,marriage.* from marriage,user as w,user as h where marriage.wmcuserid=w.user_id and marriage.hmcuserid=h.user_id")
        return render_template('clerk/clerk_marriage_status.html',data=b)
    else:
        return redirect('/login')


@app.route('/clerk_caste_status')
def clerk_caste_status():
    if session['lo'] == "li":

        db = Db()
        b = db.select("select * from caste,user WHERE caste.cuserid=user.user_id")
        return render_template('clerk/clerk_caste_status.html',data=b)
    else:
        return redirect('/login')


@app.route('/clerk_income_status')
def clerk_income_status():
    if session['lo'] == "li":

        db = Db()
        b = db.select("select * from income,user WHERE income.inc_userid=user.user_id")
        return render_template('clerk/clerk_income_status.html',data=b)
    else:
        return redirect('/login')


@app.route('/view_clerk_notification')
def view_clerk_notification():
    if session['lo'] == "li":
        db = Db()
        b = db.select("select * from notification")
        return render_template('clerk/view_clerk_notification.html',data=b)
    else:
        return redirect('/login')

@app.route('/view_clerk_feedback')
def view_clerk_feedback():
    if session['lo'] == "li":
        db = Db()
        b = db.select("select * from feedback,user where feedback.fuser_id=user.user_id")
        return render_template('clerk/view_clerk_feedback.html', data=b)

    else:
        return redirect('/login')

@app.route('/clerk_profile', methods=['GET', 'POST'])
def clerk_profile():
    if session['lo'] == "li":
        db = Db()
        ss = db.selectOne("select * from clerk WHERE login_id='" + str(session['lid']) + "'")
        return render_template("clerk/clerk_profile.html", data=ss)
    else:
        return redirect('/login')






















#FOURTH MODULE

@app.route('/user_home')
def user_home():
    if session['lo'] == "li":
        return render_template('user/user_home.html')
    else:
        return redirect('/login')


# @app.route('/user_registration')
# def user_registration1():
#     return render_template('user/user_registration.html')


@app.route('/user_registration',methods=['GET','POST'])
def user_registration():
    if request.method=='POST':
        name = request.form['textfield']
        gender = request.form['RadioGroup1']
        DOB = request.form['textfield2']
        housename = request.form['textfield3']
        place = request.form['textfield4']
        post = request.form['textfield5']
        pin = request.form['textfield6']
        district = request.form['select']
        email = request.form['textfield7']
        phoneno = request.form['textfield8']
        village = request.form['textfield9']
        taluk = request.form['textfield10']
        localbody = request.form['textfield11']
        fathersname = request.form['textfield12']
        mothersname = request.form['textfield14']
        image = request.files['fileField']
        date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        image.save(r"C:\Users\Athul\PycharmProjects\pocketcertificate\static\image\\" + date + ".jpg")
        path = ("/static/image/" + date + ".jpg")
        password = request.form['textfield13']
        confirm = request.form['textfield15']
        if password==confirm:
            db=Db()
            qry = db.insert("insert into login VALUES ('','" + email + "','" + str(password) + "','USER')")
            db.insert("insert into user values('" + str(qry) + "','" + name + "','" + gender + "','" + DOB + "','" + housename + "','" + place + "','" + post + "','" + pin + "','" + district + "','" + email + "','" + phoneno + "','" + village + "','" + taluk + "','" + localbody + "','" + fathersname + "','" + mothersname + "','"+str(path)+"')")
        else:
            return '''<script>alert('password mismatch');window.location="/login"</script>'''
        return '''<script>alert('successfull');window.location="/login"</script>'''
    else:
        return render_template('user_registration.html')


@app.route('/application_category')
def application_category():
    if session['lo'] == "li":
        db=Db()
        a=db.select("select * from department_add")
        return render_template('user/application_category.html',data=a)
    else:
        return redirect('/login')


@app.route('/upload_certificate')
def upload_certificate():
    if session['lo'] == "li":

        return render_template('user/file_upload_category.html')
    else:
        return redirect('/login')


@app.route('/upload_certificate/<ptype>',methods=['get','post'])
def upload_aadhaar_certificate(ptype):
    if session['lo'] == "li":

        if request.method=='POST':
            c=request.files['fileField']
            date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            c.save(r"C:\Users\Athul\PycharmProjects\pocketcertificate\static\certificate\\" + date + ".jpg")
            path = ("/static/certificate//" + date + ".jpg")
            f_path = "C:\\Users\\Athul\\PycharmProjects\\pocketcertificate\\static\\certificate\\" + date + ".jpg"
            # fl.save(f_path)
            obj = IMG_xor()
            pth, r_rnd, g_rnd, b_rnd = obj.enc(f_path)
            pth="/static/encrypted/"+pth
            db=Db()
            print(session['lid'])
            res=db.insert("insert into certificate VALUES ('','"+str(pth)+"','"+str(session['lid'])+"','"+ptype+"')")
            qry2 = "insert into xor_keys(certificate_id,key1,key2,key3) values('" + str(res) + "','" + str(r_rnd) + "','" + str(
                 g_rnd) + "','" + str(b_rnd) + "')"
            db.insert(qry2)
            return '''<script>alert('successfull');window.location="/upload_certificate"</script>'''
        else:
            return render_template('user/upload_certificate.html')
    else:
        return redirect('/login')


@app.route('/send_application')
def send_application():
    if session['lo'] == "li":
        return render_template('user/send_application.html')
    else:
        return redirect('/login')


@app.route('/send_caste/',methods=['get','post'])
def send_caste():
    if session['lo'] == "li":
        if request.method=='POST':
            religion=request.form['textfield']
            caste=request.form['textfield2']
            category=request.form['textfield3']
            db=Db()
            print(session['lid'])
            db.insert("insert into caste VALUES ('','"+str(session['lid'])+"','"+religion+"','"+caste+"','"+category+"','pending')")
            return '''<script>alert('successfull');window.location="/send_caste"</script>'''
        else:
            return render_template('user/send_caste_application.html')
    else:
        return redirect('/login')


@app.route('/send_income/',methods=['get','post'])
def send_income():
    if session['lo'] == "li":

        if request.method=='POST':
            source=request.form['textfield']
            amount=request.form['textfield2']
            db=Db()
            print(session['lid'])
            db.insert("insert into income VALUES ('','"+str(session['lid'])+"','"+source+"','"+amount+"','pending')")
            return '''<script>alert('successfull');window.location="/send_income"</script>'''
        else:
            return render_template('user/send_income_application.html')
    else:
        return redirect('/login')


@app.route('/send_marriage/',methods=['get','post'])
def send_marriage():
    if session['lo'] == "li":

        if request.method=='POST':
            date=request.form['textfield']
            location=request.form['textfield2']
            pe=request.form['textfield3']
            db=Db()
            print(session['lid'])
            q=db.selectOne("select * from user where email='"+pe+"'")
            if q:
                pid=q['user_id']
                gen=q['gender']
                if gen=='male':
                    db.insert("insert into marriage VALUES ('','"+str(session['lid'])+"','"+str(pid)+"','"+date+"','"+location+"','pending')")
                else:
                    db.insert("insert into marriage VALUES ('','" + str(pid) + "','" + str(session['lid']) + "','" + date + "','" + location + "','pending')")
                return '''<script>alert('successfull');window.location="/send_marriage"</script>'''
            else:
                return '''<script>alert('Partner Email Doesn't Exists');window.location="/send_marriage"</script>'''
        else:
            return render_template('user/send_marriage_application.html')
    else:
        return redirect('/login')


@app.route('/send_nativity/',methods=['get','post'])
def send_nativity():
    if session['lo'] == "li":

        if request.method=='POST':
            fname=request.form['textfield']
            fstate=request.form['textfield2']
            fdistrict= request.form['select']
            fvillage = request.form['textfield3']
            ftaluk = request.form['textfield4']
            mname = request.form['textfield5']
            mstate = request.form['textfield6']
            mdistrict = request.form['select2']
            mvillage = request.form['textfield7']
            mtaluk = request.form['textfield8']
            db=Db()
            print(session['lid'])
            db.insert("insert into nativity VALUES ('','"+str(session['lid'])+"','"+fstate+"','"+fdistrict+"','"+ftaluk+"','"+fvillage+"','"+mdistrict+"','"+mtaluk+"','"+mvillage+"','pending')")
            return '''<script>alert('successfull');window.location="/send_nativity"</script>'''
        else:
            return render_template('user/send_nativity_application.html')
    else:
        return redirect('/login')



@app.route('/user_application_status')
def user_application_status():
    if session['lo'] == "li":
         return render_template('user/user_application_status.html')
    else:
        return redirect('/login')


@app.route('/user_caste_status')
def user_caste_status():
    if session['lo'] == "li":

        db = Db()
        b = db.select("select * from caste,user WHERE caste.cuserid=user.user_id and caste.cuserid='"+str(session['lid'])+"'")
        return render_template('user/user_caste_status.html',data=b)
    else:
        return redirect('/login')


@app.route('/castecertificate/<cid>')
def castecertificate(cid):
    if session['lo'] == "li":

        db = Db()
        num=random.randint(000,999)
        d1=db.selectOne("select curdate() as d")
        a=d1['d']
        b = db.selectOne("select * from caste,user WHERE caste.cuserid=user.user_id and caste.ccid='"+cid+"'")
        return render_template("user/caste_certificate.html",a=b,n=num,d2=a)
    else:
        return redirect('/login')


@app.route('/user_marriage_status')
def user_marriage_status():
    if session['lo'] == "li":

        db = Db()
        b = db.select("select w.u_name as wn,w.dob as wdob ,w.district as wd,w.taluk as wt,w.village as wv ,h.u_name as hn,h.dob as hdob ,h.district as hd,h.taluk as ht,h.village as hv,marriage.* from marriage,user as w,user as h where marriage.wmcuserid=w.user_id and marriage.hmcuserid=h.user_id and marriage.hmcuserid='"+str(session['lid'])+"'")
        return render_template('user/user_marriage_status.html',data=b)
    else:
        return redirect('/login')


@app.route('/marriagecertificate/<cid>')
def marriagecertificate(cid):
    if session['lo'] == "li":

        db = Db()
        num=random.randint(000,999)
        d1=db.selectOne("select curdate() as d")
        a=d1['d']
        b = db.selectOne("select w.u_name as wn,w.dob as wdob ,w.district as wd,w.place as wp,w.taluk as wt,w.village as wv,w.father_name as wf,w.mother_name as wm,h.u_name as hn,h.dob as hdob ,h.district as hd,h.taluk as ht,h.village as hv,h.father_name as hf,h.mother_name as hm,marriage.* from marriage,user as w,user as h where marriage.wmcuserid=w.user_id and marriage.hmcuserid=h.user_id and marriage.mcid='"+cid+"'")

        # b = db.selectOne("select * from marriage,user WHERE marriage.wmcuserid=w.user_id  and marriage.hmcuserid=h.user_id and marriage.mcid='"+cid+"'")
        return render_template("user/marriage_certificate.html",a=b,n=num,d2=a)
    else:
        return redirect('/login')


@app.route('/user_nativity_status')
def user_nativity_status():
    if session['lo'] == "li":
        db = Db()
        b = db.select("SELECT * FROM NATIVITY,USER WHERE NATIVITY.ncuserid=user.user_id and NATIVITY.ncuserid='"+str(session['lid'])+"'")
        print(b)
        return render_template('user/user_nativity_status.html',data=b)
    else:
        return redirect('/login')


@app.route('/nativitycertificate/<cid>')
def nativitycertificate(cid):
    if session['lo'] == "li":

        db = Db()
        num=random.randint(000,999)
        d1=db.selectOne("select curdate() as d")
        a=d1['d']
        b = db.selectOne("select * from nativity,user WHERE NATIVITY.ncuserid=user.user_id and NATIVITY.ncid='"+cid+"'")
        return render_template("user/nativity_certificate.html",a=b,n=num,d2=a)
    else:
        return redirect('/login')


@app.route('/user_income_status')
def user_income_status():
    if session['lo'] == "li":
        db = Db()
        b = db.select("select * from income,user WHERE income.inc_userid=user.user_id and income.inc_userid= '"+str(session['lid'])+"'")
        return render_template('user/user_income_status.html',data=b)
    else:
        return redirect('/login')

@app.route('/incomecertificate/<cid>')
def incomecertificate(cid):
    if session['lo'] == "li":
        db = Db()
        num=random.randint(000,999)
        d1=db.selectOne("select curdate() as d")
        a=d1['d']
        b = db.selectOne("select * from income,user WHERE income.inc_userid=user.user_id AND income.inc_id='"+cid+"'")
        return render_template("user/income_certificate.html",a=b,n=num,d2=a)
    else:
        return redirect('/login')

@app.route('/send_complaint',methods=['GET','POST'])
def send_complaint():
    if session['lo'] == "li":
        if request.method=='POST':
            complaint=request.form['textarea']
            db=Db()
            q=db.insert("insert into complaint VALUES ('"+str(session['lid'])+"','"+complaint+"',curdate(),'pending','','') ")
            return  '''<script>alert("complaint send");window.location="/user_home"</script>'''
        else:
            return render_template('user/send_complaint.html')
    else:
        return redirect('/login')


@app.route('/user_view_reply')
def user_view_reply():
    if session['lo'] == "li":
        db = Db()
        b=db.select("select * from complaint,user WHERE complaint.userid=user.user_id and complaint.userid='"+str(session['lid'])+"'")
        return render_template('user/user_view_reply.html', data=b)
    else:
        return redirect('/login')


@app.route('/send_feedback',methods=['GET','POST'])
def send_feedback():
    if session['lo'] == "li":
        if request.method=='POST':
            f=request.form['textarea']
            db=Db()
            q=db.insert("insert into feedback VALUES ('','"+str(session['lid'])+"','"+f+"',curdate()) ")
            return  '''<script>alert("feedback send");window.location="/user_home"</script>'''
        else:
            return render_template('user/user_send_feedback.html')
    else:
        return redirect('/login')


@app.route('/change_password',methods=['GET','POST'])
def change_password():
    if session['lo'] == "li":
        db = Db()
        if request.method=='POST':
            current=request.form['textfield1']
            new = request.form['textfield2']
            confirm=request.form['textfield3']
            if new==confirm:
                q=db.selectOne("select * from login where login_id='"+str(session['lid'])+"'and password='"+current+"'")
                if q:
                    db.update("update login set password='"+new+"' where login_id='"+str(session['lid'])+"'")
                    return  '''<script>alert("password changed");window.location="/"</script>'''
                else:
                    return '''<script>alert("invalid user");window.location="/change_password"</script>'''
            else:
                return '''<script>alert("password mismatch");window.location="/change_password"</script>'''
        else:
            return render_template('user/user_change_password.html')
    else:
        return redirect('/login')


@app.route('/my_profile',methods=['GET','POST'])
def my_profile():
    if session['lo'] == "li":
        db=Db()
        ss=db.selectOne("select * from user WHERE user_id='"+str(session['lid'])+"'")
        return  render_template("user/my_profile.html",data=ss)
    else:
        return redirect('/login')


@app.route('/edit_profile/<p>',methods=['POST','GET'])
def edit_profile(p):
    if session['lo'] == "li":
        db=Db()
        if request.method=="POST":
            name = request.form['textfield']
            gender = request.form['RadioGroup1']
            DOB = request.form['textfield2']
            housename = request.form['textfield3']
            place = request.form['textfield4']
            post = request.form['textfield5']
            pin = request.form['textfield6']
            district = request.form['select']
            email = request.form['textfield7']
            phoneno = request.form['textfield8']
            village = request.form['textfield9']
            taluk = request.form['textfield10']
            localbody = request.form['textfield11']
            fathersname = request.form['textfield12']
            mothersname = request.form['textfield14']
            image = request.files['fileField']
            date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            image.save(r"C:\Users\Athul\PycharmProjects\pocketcertificate\static\image\\" + date + ".jpg")
            path = ("/static/image/" + date + ".jpg")
            if request.files != None:
                if image.filename != "":
                    db.update( "update user set u_name='" + name + "',gender ='" + gender + "',dob='" + DOB + "',housename='" + housename + "',place='" + place + "',post='" + post + "',pin='" + pin + "',district='" + district + "',email='" + email + "',phoneno='" + phoneno +"',village='" + village + "',taluk='" + taluk + "',name_of_local_body='" + localbody + "',father_name='" + fathersname + "',mother_name='" + mothersname + "',image='" + str(path) + "'where user_id='" + p + "'")
                    return '''<script>alert("success");window.location="/my_profile"</script>'''
                else:
                    db.update("update user set u_name='" + name + "',gender ='" + gender + "',dob='" + DOB + "',housename='" + housename + "',place='" + place + "',post='" + post + "',pin='" + pin + "',district='" + district + "',email='" + email + "',phoneno='" + phoneno +"',village='" + village + "',taluk='" + taluk + "',name_of_local_body='" + localbody + "',father_name='" + fathersname + "',mother_name='" + mothersname + "' where user_id='" + p + "'")
                    return '''<script>alert("success");window.location="/my_profile"</script>'''
            else:
                db.update("update user set u_name='" + name + "',gender ='" + gender + "',dob='" + DOB + "',housename='" + housename + "',place='" + place + "',post='" + post + "',pin='" + pin + "',district='" + district + "',email='" + email + "',phoneno='" + phoneno +"',village='" + village + "',taluk='" + taluk + "',name_of_local_body='" + localbody + "',father_name='" + fathersname + "',mother_name='" + mothersname + "' where user_id='" + p + "'")
                return '''<script>alert("success");window.location="/my_profile"</script>'''

        a=db.selectOne("select * from user where user_id='" + p + "'")

        return render_template('user/edit_profile.html',data=a)
    else:
        return redirect('/login')
















if __name__ == '__main__':
    app.run()
