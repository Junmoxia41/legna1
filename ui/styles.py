import flet as ft

# COLORES SEGUROS PARA EVITAR CUADROS GRISES
C_VOID = "#010205"
C_BG = "#030408"
C_SIDEBAR = "#07080C"
C_CYAN = "#00D9FF"
C_BLUE = "#007FFF"
C_PURPLE = "#6A5CFF"
C_TEXT = "#E0E6ED"
C_GLASS = "#11141B" # Un poco más claro para que se vea el efecto
C_BORDER = "#1E2229"

# ESTILOS DE TEXTO
S_HEADER = ft.TextStyle(font_family="SpaceGrotesk", weight="bold", color=C_CYAN)
S_BODY = ft.TextStyle(font_family="Segoe UI", color=C_TEXT)
S_HUD = ft.TextStyle(font_family="JetBrains Mono", size=10, color="#556677")

FONTS = {
    "SpaceGrotesk": "https://github.com/google/fonts/raw/main/ofl/spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf",
    "JetBrains": "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Regular.ttf"
}
