

# CRUD Routes for accessing JSON Data from database
# Malt Routes (Read/Read All Only)
@app.route('/malt', methods=['GET'])
def get_malts():
    return jsonify(database.MaltSchema(many=True).dump(database.Malt.query.all()))


@app.route('/malt/<id>', methods=['GET'])
def get_malt(id):
    return database.MaltSchema().jsonify(database.Malt.query.get(id))

# Hops Routes (Read/Read All Only)
@app.route('/hops', methods=['GET'])
def get_hops():
    return jsonify(database.HopsSchema(many=True).dump(database.Hops.query.all()))


@app.route('/hops/<id>', methods=['GET'])
def get_hop(id):
    return database.YeastSchema().jsonify(database.Yeast.query.get(id))

# Yeast Routes (Read/Read All Only)
@app.route('/yeast', methods=['GET'])
def get_yeasts():
    return jsonify(database.YeastSchema(many=True).dump(database.Yeast.query.all()))


@app.route('/yeast/<id>', methods=['GET'])
def get_yeast(id):
    return database.HopsSchema().jsonify(database.Hops.query.get(id))

# Recipe Routes (Create, Read/Read All, Update, Delete)
@app.route('/recipe', methods=['POST'])
def add_recipe():
    print('Request: {}'.format(request))
    recipe_name = request.json['recipe_name']

    recipe_method = request.json['recipe_method']
    recipe_srm = request.json['recipe_srm']
    recipe_batch_size = request.json['recipe_batch_size']
    recipe_rating = request.json['recipe_rating']
    recipe_description = request.json['recipe_description']
    style_id = request.json['style_id']
    image_id = request.json['image_id']

    recipe = database.Recipe(recipe_name, recipe_method, recipe_srm, recipe_batch_size, recipe_rating,
                             recipe_description, style_id, image_id)

    database.db.session.add(recipe)
    database.db.session.commit()

    return database.RecipeSchema().jsonify(recipe)


@app.route('/recipe', methods=['GET'])
def get_recipes():
    return jsonify(database.RecipeSchema(many=True).dump(database.Recipe.query.all()))


@app.route('/recipe/<id>', methods=['GET'])
def get_recipe(id):
    return database.RecipeSchema().jsonify(database.Recipe.query.get(id))


@app.route('recipe/<id>', methods=['PUT'])
def update_recipe(id):
    pass


@app.route('recipe/<id>', methods=['DELETE'])
def delete_recipe(id):
    pass


# Recipe Routes (Create, Read/Read All, Update, Delete)
@app.route('/recipe', methods=['POST'])
def add_recipe():
    print('Request: {}'.format(request))
    recipe_name = request.json['recipe_name']

    recipe_method = request.json['recipe_method']
    recipe_srm = request.json['recipe_srm']
    recipe_batch_size = request.json['recipe_batch_size']
    recipe_rating = request.json['recipe_rating']
    recipe_description = request.json['recipe_description']
    style_id = request.json['style_id']
    image_id = request.json['image_id']

    recipe = database.Recipe(recipe_name, recipe_method, recipe_srm, recipe_batch_size, recipe_rating,
                             recipe_description, style_id, image_id)

    database.db.session.add(recipe)
    database.db.session.commit()

    return database.RecipeSchema().jsonify(recipe)


@app.route('/recipe', methods=['GET'])
def get_recipes():
    return jsonify(database.RecipeSchema(many=True).dump(database.Recipe.query.all()))


@app.route('/recipe/<id>', methods=['GET'])
def get_recipe(id):
    return database.RecipeSchema().jsonify(database.Recipe.query.get(id))


@app.route('recipe/<id>', methods=['PUT'])
def update_recipe(id):
    pass


@app.route('recipe/<id>', methods=['DELETE'])
def delete_recipe(id):
    pass