from flask import Flask, render_template, request, url_for, redirect, flash
app= Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


#Show all restaurants
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	item = session.query(Restaurant).all()
	return render_template('restaurants.html', item = item)

#Create new restaurant
@app.route('/restaurant/new/', methods= ['GET', 'POST'])
def newRestaurant():
	if request.method =='POST':
		newItem = Restaurant(name = request.form['name'])
		session.add(newItem)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newRestaurant.html')

#Edit a restaurant
@app.route('/restaurant/<int:restaurant_id>/edit', methods= ['GET', 'POST'])
def editRestaurant(restaurant_id):
	item = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method =='POST':
		if request.form['name']:
			q = request.form['name']
			item.name = q
		session.add(item)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editRestaurant.html', item = item)

#Delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete/', methods= ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	item = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method =='POST':
		session.delete(item)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('deleteRestaurant.html', item = item)


#Show restaurant menu
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return render_template('menu.html', restaurant = restaurant, items = items)

#Create new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods= ['GET', 'POST'])
def newMenuItem(restaurant_id):
	item = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menu = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).first()
	if request.method =='POST':
		if request.form['newMenuItem']:
			newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant = menu.restaurant)
			session.add(newItem)
			session.commit()
			flash("New Menu Item Created!")
			return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newMenuItem.html', item = item)

#Edit a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods= ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	item = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menu = session.query(MenuItem).filter_by(id = menu_id).first()
	if request.method =='POST':
		if request.form['editMenuItem']:
			menu.name = request.form['name']
			menu.description = request.form['description']
			menu.price = price = request.form['price']
			Course = request.form['course']
			session.add(editItem)			
			session.commit()
			return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('editMenuItem.html', item = item, menu = menu)



#Delete menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods= ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	item = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menuItem = session.query(MenuItem).filter_by(id = menu_id).first()
	if request.method =='POST':
		session.delete(menuItem)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('deleteMenuItem.html', menuItem = menuItem, item = item)


if (__name__) == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000, threaded = True)

