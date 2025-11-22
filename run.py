from app import app


#----------------------------------------
# launch
#----------------------------------------

# Debug: print all registered routes - for me to see if blueprint routes are registered
print(app.url_map)

if __name__ == "__main__":
	app.run(debug=True, port=5001)