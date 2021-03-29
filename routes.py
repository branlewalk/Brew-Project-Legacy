from flask import jsonify, Blueprint, request
import database
import domain

# Malt Blueprint
malt_blueprint = Blueprint(
    'malt',
    __name__,
    template_folder='templates'
)


# Malt Routes (Read/Read All Only)
@malt_blueprint.route('/', methods=['GET'])
def get_malts():
    malts = database.Malt.query.all()
    malt_objects = list()
    for m in malts:
        malt_objects.append(domain.Malt(m.malt_id, m.malt_name, m.malt_origin, m.malt_category, m.malt_type,
                                        m.malt_lovibond, m.malt_ppg))
    return domain.MaltSchema(many=True).dumps(malt_objects)


def get_malt_object(malt_id):
    m = database.Malt.query.get(malt_id)
    malt_object = domain.Malt(m.malt_id, m.malt_name, m.malt_origin, m.malt_category, m.malt_type, m.malt_lovibond,
                              m.malt_ppg)
    return malt_object


@malt_blueprint.route('/<malt_id>', methods=['GET'])
def get_malt(malt_id):
    return domain.MaltSchema().dumps(get_malt_object(malt_id))


# Hops Blueprint
hops_blueprint = Blueprint(
    'hops',
    __name__,
    template_folder='templates'
)


# Hops Routes (Read/Read All Only)
@hops_blueprint.route('/', methods=['GET'])
def get_hops():
    hops = database.Hops.query.all()
    hop_objects = list()
    for h in hops:
        hop_objects.append(domain.Hops(h.hops_id, h.hops_variety, h.hops_type, h.hops_aa, h.hops_use))
    return domain.HopsSchema(many=True).dumps(hop_objects)


def get_hops_object(hops_id):
    h = database.Hops.query.get(hops_id)
    hop_object = domain.Hops(h.hops_id, h.hops_variety, h.hops_type, h.hops_aa, h.hops_use)
    return hop_object


@hops_blueprint.route('/<hops_id>', methods=['GET'])
def get_hop(hops_id):
    h = database.Hops.query.get(hops_id)
    hop_object = domain.Hops(h.hops_id, h.hops_variety, h.hops_type, h.hops_aa, h.hops_use)
    return domain.HopsSchema().dumps(get_hops_object(hops_id))


# Yeast Blueprint
yeast_blueprint = Blueprint(
    'yeast',
    __name__,
    template_folder='templates'
)


# Yeast Routes (Read/Read All Only)
@yeast_blueprint.route('/', methods=['GET'])
def get_yeasts():
    yeasts = database.Yeast.query.all()
    yeast_objects = list()
    for y in yeasts:
        yeast_objects.append(domain.Yeast(y.yeast_id, y.yeast_strain, y.yeast_lab, y.yeast_code, y.yeast_type,
                                          y.yeast_floc, y.yeast_atten, y.yeast_min_temp, y.yeast_max_temp))
    return domain.YeastSchema(many=True).dumps(yeast_objects)


def get_yeast_object(yeast_id):
    y = database.Yeast.query.get(yeast_id)
    yeast_object = domain.Yeast(y.yeast_id, y.yeast_strain, y.yeast_lab, y.yeast_code, y.yeast_type,
                                y.yeast_floc, y.yeast_atten, y.yeast_min_temp, y.yeast_max_temp)
    return yeast_object


@yeast_blueprint.route('/<yeast_id>', methods=['GET'])
def get_yeast(yeast_id):
    return domain.YeastSchema().dumps(get_yeast_object(yeast_id))


# Other Blueprint
other_blueprint = Blueprint(
    'other',
    __name__,
    template_folder='templates'
)


# Other Routes (Read/Read All Only)
@other_blueprint.route('/', methods=['GET'])
def get_others():
    others = database.Other.query.all()
    other_objects = list()
    for o in others:
        other_objects.append(domain.Other(o.other_id, o.other_name, o.other_type, o.other_use))
    return domain.OtherSchema(many=True).dumps(other_objects)


def get_other_object(other_id):
    o = database.Other.query.get(other_id)
    other_object = domain.Other(o.other_id, o.other_name, o.other_type, o.other_use)
    return other_object


@other_blueprint.route('/<other_id>', methods=['GET'])
def get_other(other_id):
    return domain.OtherSchema().dumps(get_other_object(other_id))


# Style Blueprint
style_blueprint = Blueprint(
    'style',
    __name__,
    template_folder='templates'
)


# Style Routes (Read/Read All Only)
@style_blueprint.route('/', methods=['GET'])
def get_styles():
    styles = database.Style.query.all()
    style_objects = list()
    for s in styles:
        style_objects.append(domain.Style(s.style_id, s.style_name, s.style_category, s.style_bjcp, s.style_min_ibu,
                                          s.style_max_ibu, s.style_min_abv, s.style_max_abv, s.style_min_fg,
                                          s.style_max_fg, s.style_min_co2_vol, s.style_max_co2_vol, s.style_lovibond,
                                          s.image_id))
    return domain.StyleSchema(many=True).dumps(style_objects)


def get_style_object(style_id):
    s = database.Style.query.get(style_id)
    style_object = domain.Style(s.style_id, s.style_name, s.style_category, s.style_bjcp, s.style_min_ibu,
                                s.style_max_ibu, s.style_min_abv, s.style_max_abv, s.style_min_fg, s.style_max_fg,
                                s.style_min_co2_vol, s.style_max_co2_vol, s.style_lovibond, s.image_id)
    return style_object


@style_blueprint.route('/<style_id>', methods=['GET'])
def get_style(style_id):
    return domain.StyleSchema().dumps(get_style_object(style_id))


# Image Blueprint
image_blueprint = Blueprint(
    'image',
    __name__,
    template_folder='templates'
)


# Image Routes (Read/Read All Only)
@image_blueprint.route('/', methods=['GET'])
def get_styles():
    images = database.Image.query.all()
    image_objects = list()
    for i in images:
        image_objects.append(domain.Image(i.image_id, i.image_description, i.image_url))
    return domain.StyleSchema(many=True).dumps(image_objects)


def get_image_object(image_id):
    i = database.Image.query.get(image_id)
    image_object = domain.Image(i.image_id, i.image_description, i.image_url)
    return image_object


@image_blueprint.route('/<image_id>', methods=['GET'])
def get_style(image_id):
    return domain.ImageSchema().dumps(get_image_object(image_id))


# Recipe Blueprint
recipe_blueprint = Blueprint(
    'recipe',
    __name__,
    template_folder='templates'
)


# Recipe Routes (Create, Read/Read All, Update, Delete)
@recipe_blueprint.route('/', methods=['POST'])
def add_recipe():
    recipe_name = request.json['name']
    recipe_method = request.json['method']
    recipe_batch_size = request.json['batch_size']
    recipe_rating = request.json['rating']
    recipe_description = request.json['description']
    style_id = request.json['style_id']
    image_id = request.json['image_id']
    recipe = database.Recipe(recipe_name, recipe_method, recipe_batch_size, recipe_rating,
                             recipe_description, style_id, image_id)
    database.db.session.add(recipe)
    database.db.session.commit()
    style_object = get_style_object(r.style_id)
    image_object = get_image_object(r.image_id)

    recipe_object = domain.Recipe(recipe.recipe_id, recipe_name, recipe_method, recipe_batch_size, recipe_rating,
                                  recipe_description, style_object, image_object)

    return domain.RecipeSchema().dumps(recipe_object)


@recipe_blueprint.route('/', methods=['GET'])
def get_recipes():
    recipes = database.Recipe.query.all()
    recipe_objects = list()
    for r in recipes:
        malt_ingreds = get_malt_ingred_objects(r.recipe_id)
        hops_ingreds = get_hops_ingred_objects(r.recipe_id)
        yeast_ingreds = get_yeast_ingred_objects(r.recipe_id)
        other_ingreds = get_other_ingred_objects(r.recipe_id)
        sessions = get_session_objects(r.recipe_id)
        steps = get_step_objects(r.recipe_id)
        style_object = get_style_object(r.style_id)
        image_object = get_image_object(r.image_id)
        recipe_objects.append(domain.Recipe(r.recipe_id, r.recipe_name, r.recipe_method, r.recipe_batch_size,
                                            r.recipe_rating, r.recipe_description, style_object, image_object,
                                            malt_ingreds, hops_ingreds, yeast_ingreds, other_ingreds, sessions, steps))

    return domain.RecipeSchema(many=True).dumps(recipe_objects)


@recipe_blueprint.route('/<recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    r = database.Recipe.query.get(recipe_id)
    malt_ingreds = get_malt_ingred_objects(recipe_id)
    hops_ingreds = get_hops_ingred_objects(recipe_id)
    yeast_ingreds = get_yeast_ingred_objects(recipe_id)
    other_ingreds = get_other_ingred_objects(recipe_id)
    sessions = get_session_objects(recipe_id)
    steps = get_step_objects(recipe_id)
    style_object = get_style_object(r.style_id)
    image_object = get_image_object(r.image_id)
    recipe_object = domain.Recipe(r.recipe_id, r.recipe_name, r.recipe_method, r.recipe_batch_size, r.recipe_rating,
                                  r.recipe_description, style_object, image_object, malt_ingreds, hops_ingreds,
                                  yeast_ingreds, other_ingreds, sessions, steps)
    return domain.RecipeSchema().dumps(recipe_object)


@recipe_blueprint.route('/<recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    r = database.Recipe.query.get(recipe_id)
    r.recipe_name = request.json['name']
    r.recipe_method = request.json['method']
    r.recipe_srm = request.json['srm']
    r.recipe_batch_size = request.json['batch_size']
    r.recipe_rating = request.json['rating']
    r.recipe_description = request.json['description']
    r.style_id = request.json['style_id']
    r.image_id = request.json['image_id']
    database.db.session.commit()
    malt_ingreds = get_malt_ingred_objects(recipe_id)
    hops_ingreds = get_hops_ingred_objects(recipe_id)
    yeast_ingreds = get_yeast_ingred_objects(recipe_id)
    other_ingreds = get_other_ingred_objects(recipe_id)
    sessions = get_session_objects(recipe_id)
    steps = get_step_objects(recipe_id)
    style_object = get_style_object(r.style_id)
    image_object = get_image_object(r.image_id)
    recipe_object = domain.Recipe(r.recipe_id, r.recipe_name, r.recipe_method, r.recipe_batch_size, r.recipe_rating,
                                  r.recipe_description, style_object, image_object, malt_ingreds, hops_ingreds,
                                  yeast_ingreds, other_ingreds, sessions, steps)

    return domain.RecipeSchema().dumps(recipe_object)


@recipe_blueprint.route('/<recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    r = database.Recipe.query.get(recipe_id)
    database.db.session.delete(r)
    database.db.session.commit()
    malt_ingreds = get_malt_ingred_objects(recipe_id)
    hops_ingreds = get_hops_ingred_objects(recipe_id)
    yeast_ingreds = get_yeast_ingred_objects(recipe_id)
    other_ingreds = get_other_ingred_objects(recipe_id)
    sessions = get_session_objects(recipe_id)
    steps = get_step_objects(recipe_id)
    style_object = get_style_object(r.style_id)
    image_object = get_image_object(r.image_id)
    recipe_object = domain.Recipe(r.recipe_id, r.recipe_name, r.recipe_method, r.recipe_batch_size, r.recipe_rating,
                                  r.recipe_description, style_object, image_object, malt_ingreds, hops_ingreds,
                                  yeast_ingreds, other_ingreds, sessions, steps)
    return domain.RecipeSchema().dumps(recipe_object)


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
    mi_qty = request.json['quantity']
    mi = database.MaltIngredient(mi_qty, malt_id, recipe_id)
    database.db.session.add(mi)
    database.db.session.commit()
    mi_object = domain.MaltIngredient(mi.malt_ingred_id, get_malt_object(mi.malt_id), mi.malt_ingred_qty, mi.recipe_id)

    return domain.MaltIngredientSchema().dumps(mi_object)


def get_malt_ingred_objects(recipe_id):
    mis = database.MaltIngredient.query.filter(database.MaltIngredient.recipe_id == recipe_id).all()
    mi_objects = list()
    for mi in mis:
        mi_objects.append(domain.MaltIngredient(mi.malt_ingred_id, get_malt_object(mi.malt_id), mi.malt_ingred_qty,
                                                mi.recipe_id))
    return mi_objects


@malt_ingred_blueprint.route('/malts/<recipe_id>', methods=['GET'])
def get_malt_ingreds(recipe_id):
    mi_objects = get_malt_ingred_objects(recipe_id)
    return domain.MaltIngredientSchema().dumps(mi_objects, many=True)


@malt_ingred_blueprint.route('/<malt_ingred_id>', methods=['GET'])
def get_malt_ingred(malt_ingred_id):
    mi = database.MaltIngredient.query.get(malt_ingred_id)
    mi_object = domain.MaltIngredient(mi.malt_ingred_id, get_malt_object(mi.malt_id), mi.malt_ingred_qty, mi.recipe_id)
    return domain.MaltIngredientSchema().dumps(mi_object)


@malt_ingred_blueprint.route('/<malt_ingred_id>', methods=['PUT'])
def update_malt_ingred(malt_ingred_id):
    mi = database.MaltIngredient.query.get(malt_ingred_id)
    mi.malt_id = request.json['malt_id']
    mi.recipe_id = request.json['recipe_id']
    mi.malt_ingred_qty = request.json['quantity']
    database.db.session.commit()
    mi_object = domain.MaltIngredient(mi.malt_ingred_id, get_malt_object(mi.malt_id), mi.malt_ingred_qty, mi.recipe_id)
    return domain.MaltIngredientSchema().dumps(mi_object)


@malt_ingred_blueprint.route('/<malt_ingred_id>', methods=['DELETE'])
def delete_malt_igred(malt_ingred_id):
    mi = database.MaltIngredient.query.get(malt_ingred_id)
    database.db.session.delete(mi)
    database.db.session.commit()
    mi_object = domain.MaltIngredient(mi.malt_ingred_id, get_malt_object(mi.malt_id), mi.malt_ingred_qty, mi.recipe_id)
    return database.MaltIngredientSchema().dumps(mi_object)


# Hops Ingredient Blueprint
hops_ingred_blueprint = Blueprint(
    'hops_ingred',
    __name__,
    template_folder='templates'
)


# Hops Ingredient Routes (Create, Read/Read All, Update, Delete)
@hops_ingred_blueprint.route('/', methods=['POST'])
def add_hops_ingred():
    hops_id = request.json['hops_id']
    recipe_id = request.json['recipe_id']
    hi_qty = request.json['quantity']
    hops_time = request.json['hops_time']
    hi = database.HopsIngredient(hi_qty, hops_time, hops_id, recipe_id)
    database.db.session.add(hi)
    database.db.session.commit()
    hi_object = domain.HopsIngredient(hi.hops_ingred_id, get_hops_object(hi.hops_id), hi.hops_ingred_qty, hi.hops_time, hi.recipe_id)
    return database.HopsIngredientSchema().dumps(hi_object)


def get_hops_ingred_objects(recipe_id):
    his = database.HopsIngredient.query.filter(database.HopsIngredient.recipe_id == recipe_id).all()
    hi_objects = list()
    for hi in his:
        hi_objects.append(
            domain.HopsIngredient(hi.hops_ingred_id, get_hops_object(hi.hops_id), hi.hops_ingred_qty, hi.hops_time, hi.recipe_id))
    return hi_objects


@hops_ingred_blueprint.route('/<recipe_id>', methods=['GET'])
def get_hops_ingreds(recipe_id):
    hi_objects = get_hops_ingred_objects(recipe_id)
    return domain.HopsIngredientSchema().dumps(hi_objects, many=True)


@hops_ingred_blueprint.route('/<hops_ingred_id>', methods=['GET'])
def get_hops_ingred(hops_ingred_id):
    hi = database.HopsIngredient.query.get(hops_ingred_id)
    hi_object = domain.HopsIngredient(hi.hops_ingred_id, get_hops_object(hi.hops_id), hi.hops_ingred_qty, hi.hops_time, hi.recipe_id)
    return domain.HopsIngredientSchema().dumps(hi_object)


@hops_ingred_blueprint.route('/<hops_ingred_id>', methods=['PUT'])
def update_hops_ingred(hops_ingred_id):
    hi = database.HopsIngredient.query.get(hops_ingred_id)
    hi.hops_id = request.json['hops_id']
    hi.recipe_id = request.json['recipe_id']
    hi.hops_ingred_qty = request.json['hops_ingred_qty']
    hi.hops_time = request.json['hops_time']
    database.db.session.commit()
    hi_object = domain.HopsIngredient(hi.hops_ingred_id, get_hops_object(hi.hops_id), hi.hops_ingred_qty, hi.hops_time, hi.recipe_id)
    return domain.HopsIngredientSchema().dumps(hi_object)


@hops_ingred_blueprint.route('/<hops_ingred_id>', methods=['DELETE'])
def delete_hops_ingred(hops_ingred_id):
    hi = database.HopsIngredient.query.get(hops_ingred_id)
    database.db.session.delete(hi)
    database.db.session.commit()
    hi_object = domain.HopsIngredient(hi.hops_ingred_id, get_hops_object(hi.hops_id), hi.hops_ingred_qty, hi.hops_time, hi.recipe_id)
    return database.HopsIngredientSchema().dumps(hi_object)


# Yeast Ingredient Blueprint
yeast_ingred_blueprint = Blueprint(
    'yeast_ingred',
    __name__,
    template_folder='templates'
)


# Yeast Ingredient Routes (Create, Read/Read All, Update, Delete)
@yeast_ingred_blueprint.route('/', methods=['POST'])
def add_yeast_ingred():
    yeast_id = request.json['yeast_id']
    recipe_id = request.json['recipe_id']
    yeast_ingred_qty = request.json['quantity']
    yeast_ingred_starter = request.json['starter']

    yeast_ingred = database.yeastIngredient(yeast_id, recipe_id, yeast_ingred_qty, yeast_ingred_starter)
    database.db.session.add(yeast_ingred)
    database.db.session.commit()

    return database.YeastIngredientSchema().jsonify(yeast_ingred)


def get_yeast_ingred_objects(recipe_id):
    pass


@yeast_ingred_blueprint.route('/<recipe_id>', methods=['GET'])
def get_yeast_ingreds(recipe_id):
    return database.YeastIngredientSchema().jsonify(database.YeastIngredient.query.get(recipe_id))


@yeast_ingred_blueprint.route('/<yeast_ingred_id>', methods=['GET'])
def get_yeast_ingred(yeast_ingred_id):
    return database.YeastIngredientSchema().jsonify(database.YeastIngredient.query.get(yeast_ingred_id))


@yeast_ingred_blueprint.route('/<yeast_ingred_id>', methods=['PUT'])
def update_yeast_ingred(yeast_ingred_id):
    yeast_ingred = database.YeastIngredient.query.get(yeast_ingred_id)
    yeast_ingred.yeast_id = request.json['yeast_id']
    yeast_ingred.recipe_id = request.json['recipe_id']
    yeast_ingred.yeast_ingred_qty = request.json['yeast_ingred_qty']
    yeast_ingred.yeast_ingred_starter = request.json['yeast_ingred_starter']
    database.db.session.commit()

    return database.YeastIngredientSchema().jsonify(yeast_ingred)


@yeast_ingred_blueprint.route('/<yeast_ingred_id>', methods=['DELETE'])
def delete_yeast_ingred(yeast_ingred_id):
    yeast_ingred = database.YeastIngredient.query.get(yeast_ingred_id)
    database.db.session.delete(yeast_ingred)
    database.db.session.commit()

    return database.YeastIngredientSchema().jsonify(yeast_ingred)


# Other Ingredient Blueprint
other_ingred_blueprint = Blueprint(
    'other_ingred',
    __name__,
    template_folder='templates'
)


# Other Ingredient Routes (Create, Read/Read All, Update, Delete)
@other_ingred_blueprint.route('/', methods=['POST'])
def add_other_ingred():
    other_id = request.json['other_id']
    recipe_id = request.json['recipe_id']
    other_ingred_qty = request.json['other_ingred_qty']
    other_ingred = database.OtherIngredient(other_id, recipe_id, other_ingred_qty)
    database.db.session.add(other_ingred)
    database.db.session.commit()

    return database.OtherIngredientSchema().jsonify(other_ingred)


def get_other_ingred_objects(recipe_id):
    pass


# TODO Looks ups for OtherIngredients - additional?
@other_ingred_blueprint.route('/<recipe_id>', methods=['GET'])
def get_other_ingreds(recipe_id):
    return database.OtherIngredientSchema().jsonify(database.OtherIngredient.query.get(recipe_id))


@other_ingred_blueprint.route('/<other_ingred_id>', methods=['GET'])
def get_other_ingred(other_ingred_id):
    return database.OtherIngredientSchema().jsonify(database.OtherIngredient.query.get(other_ingred_id))


@other_ingred_blueprint.route('/<other_ingred_id>', methods=['PUT'])
def update_other_ingred(other_ingred_id):
    other_ingred = database.OtherIngredient.query.get(other_ingred_id)
    other_ingred.other_id = request.json['other_id']
    other_ingred.recipe_id = request.json['recipe_id']
    other_ingred.other_ingred_qty = request.json['other_ingred_qty']
    database.db.session.commit()

    return database.OtherIngredientSchema().jsonify(other_ingred)


@other_ingred_blueprint.route('/<other_ingred_id>', methods=['DELETE'])
def delete_other_ingred(other_ingred_id):
    other_ingred = database.OtherIngredient.query.get(other_ingred_id)
    database.db.session.delete(other_ingred)
    database.db.session.commit()

    return database.OtherIngredientSchema().jsonify(other_ingred)


# Session Ingredient Blueprint
session_blueprint = Blueprint(
    'session',
    __name__,
    template_folder='templates'
)


# Session Routes (Create, Read/Read All, Update, Delete)
@session_blueprint.route('/', methods=['POST'])
def add_session():
    session_name = request.json['session_name']
    session_start = request.json['session_start']
    session_end = request.json['session_end']
    recipe_id = request.json['recipe_id']
    session = database.Session(session_name, session_start, session_end, recipe_id)
    database.db.session.add(session)
    database.db.session.commit()

    return database.SessionSchema().jsonify(session)


def get_session_objects(recipe_id):
    pass


@session_blueprint.route('/', methods=['GET'])
def get_session():
    return jsonify(database.SessionSchema(many=True).dump(database.Session.query.all()))


@session_blueprint.route('/<session_id>', methods=['GET'])
def get_temp(session_id):
    return database.SessionSchema().jsonify(database.Session.query.get(session_id))


# Not sure if this is needed
@session_blueprint.route('/<session_id>', methods=['PUT'])
def update_session(session_id):
    session = database.Recipe.query.get(session_id)
    session.session_name = request.json['session_name']
    session.session_start = request.json['session_start']
    session.session_end = request.json['session_end']
    session.recipe_id = request.json['recipe_id']
    database.db.session.commit()

    return database.SessionSchema().jsonify(session)


@session_blueprint.route('/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    session = database.Session.query.get(session_id)
    database.db.session.delete(session)
    database.db.session.commit()

    return database.SessionSchema().jsonify(session)


# Temps Ingredient Blueprint
temps_blueprint = Blueprint(
    'temps',
    __name__,
    template_folder='templates'
)


# Temp Routes (Create, Read/Read All, Update, Delete)
@temps_blueprint.route('/', methods=['POST'])
def add_temps():
    temp_hlt = request.json['temp_hlt']
    temp_mlt = request.json['temp_mlt']
    temp_bk = request.json['temp_bk']
    session_id = request.json['session_id']
    temps = database.Temps(temp_hlt, temp_mlt, temp_bk, session_id)
    database.db.session.add(temps)
    database.db.session.commit()

    return database.TempsSchema().jsonify(temps)


@temps_blueprint.route('/', methods=['GET'])
def get_temps():
    return jsonify(database.TempsSchema(many=True).dump(database.Temps.query.all()))


@temps_blueprint.route('/<temp_id>', methods=['GET'])
def get_temp(temp_id):
    return database.TempsSchema().jsonify(database.Temps.query.get(temp_id))


@temps_blueprint.route('/<temp_id>', methods=['PUT'])
def update_temps(temp_id):
    temps = database.Recipe.query.get(temp_id)
    temps.temp_hlt = request.json['temp_hlt']
    temps.temp_mlt = request.json['temp_mlt']
    temps.temp_bk = request.json['temp_bk']
    temps.session_id = request.json['session_id']
    database.db.session.commit()

    return database.TempsSchema().jsonify(temps)


@temps_blueprint.route('/<temp_id>', methods=['DELETE'])
def delete_temps(temp_id):
    temps = database.Temps.query.get(temp_id)
    database.db.session.delete(temps)
    database.db.session.commit()

    return database.TempsSchema().jsonify(temps)


# Step Ingredient Blueprint
step_blueprint = Blueprint(
    'step',
    __name__,
    template_folder='templates'
)


# Step Routes (Create, Read/Read All, Update, Delete)
@step_blueprint.route('/', methods=['POST'])
def add_step():
    step_name = request.json['step_name']
    step_kettle = request.json['step_kettle']
    step_temp = request.json['step_temp']
    step_timer = request.json['step_timer']
    recipe_id = request.json['recipe_id']

    step = database.Step(step_name, step_kettle, step_temp, step_timer, recipe_id)

    database.db.session.add(step)
    database.db.session.commit()

    return database.StepSchema().jsonify(step)


def get_step_objects(recipe_id):
    pass


@step_blueprint.route('/', methods=['GET'])
def get_step():
    return jsonify(database.StepSchema(many=True).dump(database.Step.query.all()))


@step_blueprint.route('/<step_id>', methods=['GET'])
def get_temp(step_id):
    return database.StepSchema().jsonify(database.Step.query.get(step_id))


@step_blueprint.route('/<step_id>', methods=['PUT'])
def update_step(step_id):
    step = database.Recipe.query.get(step_id)
    step.step_id = request.json['step_id']
    step.step_name = request.json['step_name']
    step.step_kettle = request.json['step_kettle']
    step.step_temp = request.json['step_temp']
    step.step_timer = request.json['step_timer']
    step.recipe_id = request.json['recipe_id']
    database.db.session.commit()

    return database.StepSchema().jsonify(step)


@step_blueprint.route('/<step_id>', methods=['DELETE'])
def delete_step(step_id):
    step = database.Step.query.get(step_id)
    database.db.session.delete(step)
    database.db.session.commit()

    return database.StepSchema().jsonify(step)


# Session Step Blueprint
session_step_blueprint = Blueprint(
    'session_step',
    __name__,
    template_folder='templates'
)


# Session Step Routes (Create, Read/Read All, Update, Delete)
@session_step_blueprint.route('/', methods=['POST'])
def add_session_step():
    step_id = request.json['step_id']
    session_id = request.json['session_id']
    session_step_start = request.json['session_step_start']
    session_step_end = request.json['session_step_end']
    session_step = database.SessionStep(step_id, session_id, session_step_start, session_step_end)

    database.db.session.add(session_step)
    database.db.session.commit()

    return database.SessionStepSchema().jsonify(session_step)


# TODO Gets for Associative Entities
# Who is going to need to see an all?
@session_step_blueprint.route('/<session_id>', methods=['GET'])
def get_session_steps(session_id):
    return database.SessionStepSchema().jsonify(database.SessionStep.query.get(session_id))


@session_step_blueprint.route('/<session_step_id>', methods=['GET'])
def get_session_step(session_step_id):
    return database.SessionStepSchema().jsonify(database.SessionStep.query.get(session_step_id))


# Not sure if this is needed?
@session_step_blueprint.route('/<session_step_id>', methods=['PUT'])
def update_session_step(session_step_id):
    session_step = database.SessionStep.query.get(session_step_id)
    session_step.step_id = request.json['step_id']
    session_step.session_id = request.json['session_id']
    session_step.session_step_start = request.json['session_step_start']
    session_step.session_step_end = request.json['session_step_end']

    database.db.session.commit()

    return database.SessionStepSchema().jsonify(session_step)


@session_step_blueprint.route('/<session_step_id>', methods=['DELETE'])
def delete_session_step(session_step_id):
    session_step = database.SessionStep.query.get(session_step_id)
    database.db.session.delete(session_step)
    database.db.session.commit()

    return database.SessionStepSchema().jsonify(session_step)
