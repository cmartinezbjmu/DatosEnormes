import dash_bootstrap_components as dbc
def Navbar():
   navbar = dbc.NavbarSimple(className="encabezado",
      children=[
         dbc.NavItem(dbc.NavLink("Entrenamiento", href="/apps/model")),
	 dbc.NavItem(dbc.NavLink("Muestra", href="/apps/sample"))
      ],
      brand="Home",
      brand_href="/",
      sticky="top",
   )
   return navbar
