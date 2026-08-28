<p align="center">
  <img src="assets/identity.svg" width="768"
       alt="Sofía Rodríguez, estudiante de Ingeniería Civil Informática. Trabaja en software, frontend, IA y datos.">
</p>

```text
┌───────────────────────────────────────────────────┐
│ role      ingeniería civil informática (en curso) │
│ focus     software · frontend · ia · datos        │
│ building  mapa de campus en react + typescript    │
│ learning  análisis de datos · agentes de ia       │
│ location  chile                                   │
└───────────────────────────────────────────────────┘
```

Estoy en el tramo en que aprender a programar deja de ser el objetivo y pasa a ser la
herramienta: me interesa que lo que construyo tenga una arquitectura que se pueda
sostener, decisiones que pueda defender y una interfaz que alguien más quiera usar.

<p align="center">
  <img src="assets/activity.svg" width="768"
       alt="Calendario de contribuciones de GitHub del último año, dibujado como una grilla de 53 semanas por 7 días.">
</p>

## ~/construyendo

Reparto mi trabajo en dos cuentas: esta es la principal y en
[@sofiatrops](https://github.com/sofiatrops) viven los proyectos de universidad. Cada
proyecto dice dónde está.

**[Benthos Environmental Platform](https://github.com/sofiatrops/Benthos)** · plataforma multiempresa de gestión ambiental · [@sofiatrops](https://github.com/sofiatrops)<br>
Backend en .NET sobre PostgreSQL + PostGIS, como monolito modular con Clean Architecture
y CQRS. Lo interesante está en el aislamiento entre empresas: el tenant se deriva del JWT
y baja hasta **Row-Level Security** de Postgres, así que un descuido en la aplicación no
alcanza para filtrar datos de otro cliente — lo impide la base misma. Los archivos nunca
atraviesan la API: se suben y descargan con URLs firmadas de vida corta contra
almacenamiento S3. Portal en Angular con login OIDC contra Keycloak, worker para trabajo
en segundo plano y las decisiones de diseño escritas como ADR.<br>
`C#` `.NET` `PostgreSQL` `PostGIS` `EF Core` `MediatR` `Angular` `Keycloak` `Docker` `xUnit` `Testcontainers`

**[Mapa de Campus UCT](https://github.com/sofiarodrigueznog/test-mapa)** · navegación e información para los campus de la universidad<br>
Corre sobre los planos isométricos oficiales con Leaflet en `CRS.Simple`: las coordenadas
del dominio son píxeles del plano y no latitud/longitud. Es una decisión con costo — no
hay GPS real — a cambio de conservar la identidad visual de los planos y llegar al detalle
de sala. Las rutas peatonales se resuelven con **Dijkstra** sobre un grafo de caminos, y
la conversión entre sistemas de coordenadas vive aislada en un módulo, para que un error
de proyección tenga un solo lugar donde buscarse. 55 pruebas.<br>
`React` `TypeScript` `Vite` `Tailwind` `Leaflet` `TanStack Query` `Zustand` `Zod` `Vitest`

**[Buscador semántico](https://github.com/sofiatrops/EID-Algebra-Lineal)** · recuperación de documentos con álgebra lineal · [@sofiatrops](https://github.com/sofiatrops)<br>
Cada documento de un corpus se convierte en un vector TF-IDF y la consulta se compara
midiendo el coseno del ángulo entre vectores. La vectorización y la similitud están
escritas sobre `numpy` y no delegadas a una librería que ya las resuelve: el punto era
entender por qué el método funciona antes de usarlo.<br>
`Python` `numpy` `pytest` `matplotlib`

## ~/stack

Lo que he usado construyendo, no lo que he leído.

| área | herramientas |
|---|---|
| **lenguajes** | `TypeScript` `Python` `C#` `JavaScript` `SQL` `PHP` |
| **frontend** | `React` `Angular` `Vite` `Tailwind CSS` `TanStack Query` `Zustand` `Zod` `Leaflet` |
| **backend** | `.NET` `EF Core` `MediatR` `Hangfire` `SQLAlchemy` |
| **datos** | `PostgreSQL` `PostGIS` `MySQL` `SQLite` `numpy` `pandas` `matplotlib` |
| **infra y calidad** | `Docker` `Keycloak` `GitHub Actions` `xUnit` `Vitest` `pytest` `Testcontainers` |
| **criterio** | Clean Architecture · DDD · CQRS · SOLID · patrones de diseño · modelado de datos |

## ~/aprendiendo

```text
aprendiendo/
├── datos/       análisis y visualización · Google Data Analytics
├── ia/          agentes conectados a bases de datos empresariales
├── software/    clean code · SOLID · patrones de diseño
└── frontend/    interfaces accesibles · arquitectura de componentes
```

No es una lista de cursos por completar: cada rama entra a los proyectos apenas la
entiendo lo suficiente como para defender la decisión.

<!-- TODO (Sofía): si quieres, agrega acá tus enlaces de contacto. Por ejemplo:
     [LinkedIn](https://www.linkedin.com/in/tu-usuario) · [correo](mailto:tu@correo.cl)
     No dejo ninguno puesto para no inventar datos. -->

---

<sub>El encabezado y el calendario son SVG generados por
<a href="scripts/build.py"><code>scripts/build.py</code></a> con la librería estándar de
Python: sin dependencias, sin servicios externos y sin token. Un
<a href=".github/workflows/activity.yml">workflow diario</a> los redibuja y publica
únicamente cuando la actividad cambió.</sub>
