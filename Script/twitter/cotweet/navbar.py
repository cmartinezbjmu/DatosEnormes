import dash_bootstrap_components as dbc
def Navbar():
   navbar = dbc.NavbarSimple(className="encabezado",
      children=[
         dbc.NavItem(dbc.NavLink("Entrenamiento", href="/apps/model")),
	      dbc.NavItem(dbc.NavLink("Temas", href="/apps/temas")),
         dbc.NavItem(dbc.NavLink("Modelos", href="/apps/prediccion"))
      ],
      brand="Home",
      brand_href="/",
      sticky="top",
   )
   return navbar
