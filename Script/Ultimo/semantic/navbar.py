import dash_bootstrap_components as dbc
def Navbar():
   navbar = dbc.NavbarSimple(className="encabezado",
      children=[
         dbc.NavItem(dbc.NavLink("Panel de Control", href="/apps/panel")),         
         dbc.NavItem(dbc.NavLink("Similitud", href="/apps/model")),
         dbc.NavItem(dbc.NavLink("Red politicos", href="/apps/prediccion")),         
         dbc.NavItem(dbc.NavLink("Distribución noticias/tweets", href="/apps/analisis")),
         dbc.NavItem(dbc.NavLink("Correlación", href="/apps/top_temas"))
      ],
      brand="Home",
      brand_href="/",
      sticky="top",
   )
   return navbar
