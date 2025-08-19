import flet as ft
from flet_geolocator import Geolocator, GeolocatorSettings, GeolocatorPositionAccuracy

async def main(page: ft.Page):
    page.title = "Ubicación GPS"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.theme_mode = ft.ThemeMode.LIGHT
    page.appbar = ft.AppBar(title=ft.Text("Captura de Ubicación"))

    # Texto para mostrar resultados
    result_text = ft.Text("", size=16)

    # Instancia del geolocalizador
    geolocator = Geolocator(
        location_settings=GeolocatorSettings(
            accuracy=GeolocatorPositionAccuracy.BEST
        ),
        on_error=lambda e: page.snack_bar.open(ft.SnackBar(ft.Text(f"Error: {e.data}"))),
    )
    page.overlay.append(geolocator)

    # Botón para solicitar permisos
    async def request_permission(e):
        status = await geolocator.request_permission_async(wait_timeout=30)
        result_text.value = f"Permiso: {status}"
        await page.update_async()

    # Botón para obtener ubicación actual
    async def get_location(e):
        enabled = await geolocator.is_location_service_enabled_async()
        if not enabled:
            result_text.value = "Servicio de ubicación deshabilitado"
        else:
            position = await geolocator.get_current_position_async()
            lat, lon = position.latitude, position.longitude
            result_text.value = f"Latitud: {lat}\nLongitud: {lon}\n\n📍 https://maps.google.com/?q={lat},{lon}"
        await page.update_async()

    # UI
    page.add(
        ft.Column(
            controls=[
                ft.ElevatedButton("Solicitar permiso de ubicación", on_click=request_permission),
                ft.ElevatedButton("Obtener ubicación actual", on_click=get_location),
                result_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
    )

ft.app(target=main)
