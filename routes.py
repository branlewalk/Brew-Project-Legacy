from flask import jsonify, Blueprint, request
import database

# Recipe Blueprint
recipe_blueprint = Blueprint(
    'recipe',
    __name__,
    template_folder='templates'
)

# Recipe Routes (Create, Read/Read All, Update, Delete)
@recipe_blueprint.route('/', methods=['POST'])
def add_recipe():
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


@recipe_blueprint.route('/', methods=['GET'])
def get_recipes():
    return jsonify(database.RecipeSchema(many=True).dump(database.Recipe.query.all()))


@recipe_blueprint.route('/<recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    return database.RecipeSchema().jsonify(database.Recipe.query.get(recipe_id))


@recipe_blueprint.route('/<recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    recipe = database.Recipe.query.get(recipe_id)
    recipe.recipe_name = request.json['recipe_name']
    recipe.recipe_method = request.json['recipe_method']
    recipe.recipe_srm = request.json['recipe_srm']
    recipe.recipe_batch_size = request.json['recipe_batch_size']
    recipe.recipe_rating = request.json['recipe_rating']
    recipe.recipe_description = request.json['recipe_description']
    recipe.style_id = request.json['style_id']
    recipe.image_id = request.json['image_id']
    database.db.session.commit()

    return database.RecipeSchema().jsonify(recipe)


@recipe_blueprint.route('/<recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = database.Recipe.query.get(recipe_id)
    database.db.session.delete(recipe)
    database.db.session.commit()

    return database.RecipeSchema().jsonify(recipe)


# Malt Ingredient Blueprint
malt_ingred_blueprint = Blueprint(
    'malt_ingred',
    __name__,
    template_folder='templates'
)

# Malt Ingredient Routes (Create, Read/Read All, Update, Delete)
@malt_ingred_blueprint.route('/', methods=['POST'])
def add_malt_ingred():
    malt_id = request.json['malt_id']
    recipe_id = request.json['recipe_id']
    malt_ingred_qty = request.json['malt_ingred_qty']
    malt_ingred = database.MaltIngredient(malt_id, recipe_id, malt_ingred_qty)

    database.db.session.add(malt_ingred)
    database.db.session.commit()

    return database.MaltIngredientSchema().jsonify(malt_ingred)


@malt_ingred_blueprint.route('/', methods=['GET'])
def get_malt_ingreds():
    return jsonify(database.MaltIngredientSchema(many=True).dump(database.MaltIngredient.query.all()))


@malt_ingred_blueprint.route('/<malt_id><recipe_id>', methods=['GET'])
def get_malt_ingred(malt_id, recipe_id):
    return database.MaltIngredientSchema().jsonify(database.MaltIngredient.query.get({"malt_id": malt_id,
                                                                                      "recipe_id": recipe_id}))


@malt_ingred_blueprint.route('/<malt_id><recipe_id>', methods=['PUT'])
def update_malt_ingred(malt_id, recipe_id):
    malt_ingred = database.MaltIngredient.query.get({"malt_id": malt_id, "recipe_id": recipe_id})
    malt_ingred.malt_id = request.json['malt_id']
    malt_ingred.recipe_id = request.json['recipe_id']
    malt_ingred.malt_ingred_qty = request.json['malt_ingred_qty']

    database.db.session.commit()

    return database.MaltIngredientSchema().jsonify(malt_ingred)


@malt_ingred_blueprint.route('/<malt_id><recipe_id>', methods=['DELETE'])
def delete_recipe(malt_id, recipe_id):
    malt_ingred = database.MaltIngredient.query.get({"malt_id": malt_id, "recipe_id": recipe_id})
    database.db.session.delete(malt_ingred)
    database.db.session.commit()

    return database.MaltIngredientSchema().jsonify(malt_ingred)