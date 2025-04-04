{
    "name": "Certification",
    "version": "18.0",

    "author": "Pawan Kumar",
    'sequence':-100,
    "depends": ['base', 'mail'],
    "data": [
        "security/ir.model.access.csv",
        'views/certificate_view.xml',
        'views/country_origin_view.xml',
        'views/description_form_view.xml',
        'views/menus.xml',

        
    ],
    'images': ['static/description/icon.png'],
    "auto_install": False,
    "license": "LGPL-3",
    "application": True,
    "installable": True,
}
