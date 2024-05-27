{
    "name": "Real Estate",
    "summary": "Test module",
    "version": "17.0.0.0.0",
    "license": "OEEL-1",
    "depends": ["base", "mail"],
    "application": True,
    "data": [
        "security/estate_groups.xml",
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menu.xml",
        "views/res_users_inherit_views.xml",
    ],
    "demo": []
}
