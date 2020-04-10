import dash_bootstrap_components as dbc
def Navbar():
   navbar = dbc.NavbarSimple(className="encabezado",
      children=[
         dbc.NavItem(dbc.NavLink("Etiquetado", href="/apps/model"))
      ],
      brand="Home",
      brand_href="/",
      sticky="top",
   )
   return navbar
