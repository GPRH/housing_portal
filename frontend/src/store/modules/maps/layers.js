const DOMAIN = process.env.VUE_APP_DOMAIN;

const DRONE_DOMAIN =
    process.env.NODE_ENV === "development" ? "http://localhost:8000" : DOMAIN;

export const sources = {
    aoi: {
        type: "vector",
        tiles: [DOMAIN + "/api/geodata/aoi/{id}/.mvt?tile={z}/{x}/{y}&id={id}"]
    },
    sectors: {
        type: "vector",
        tiles: [
            DOMAIN + "/api/geodata/sectors/{id}/.mvt?tile={z}/{x}/{y}&aoi_id={id}"
        ]
    },
    "sector-labels": {
        type: "geojson",
        data: DOMAIN + "/api/geodata/sectorlabels/?aoi_id={id}"
    },
    blocks: {
        type: "vector",
        tiles: [
            DOMAIN + "/api/geodata/blocks/{id}/.mvt?tile={z}/{x}/{y}&aoi_id={id}"
        ]
    },
    roads: {
        type: "vector",
        tiles: [
            DOMAIN + "/api/geodata/roads/{id}/.mvt?tile={z}/{x}/{y}&aoi_id={id}"
        ]
    },
    "clustered-buildings": {
        type: "vector",
        tiles: [
            DOMAIN +
            "/api/geodata/clustered-buildings/{id}/.mvt?tile={z}/{x}/{y}&aoi_id={id}"
        ]
    },
    buildings: {
        type: "vector",
        tiles: [
            DOMAIN + "/api/geodata/buildings/{id}/.mvt?tile={z}/{x}/{y}&aoi_id={id}"
        ]
    },
    plots: {
        type: "vector",
        tiles: [
            DOMAIN + "/api/geodata/plots/{id}/.mvt?tile={z}/{x}/{y}&aoi_id={id}"
        ]
    },
    greenspace: {
        type: "vector",
        tiles: [
            DOMAIN + "/api/geodata/greenspace/{id}/.mvt?tile={z}/{x}/{y}&aoi_id={id}"
        ]
    },
    mapillary: {
        type: "vector",
        tiles: ["https://tiles3.mapillary.com/v0.1/{z}/{x}/{y}.mvt"],
        minzoom: 0,
        maxzoom: 14
    }
};

export const layers = [{
        id: "aoi",
        name: "Area of Interest",
        checked: true,
        switcher: true,
        aois: [
            "el-pozon",
            "neiva",
            "brena",
            "chacarita",
            "tacumbu",
            "juchitan",
            "salina-cruz",
            "padang",
            "independencia"
        ],
        source: sources["aoi"],
        "source-layer": "default",
        layout: {
            visibility: "visible"
        },
        type: "fill",
        paint: {
            "fill-outline-color": "red",
            "fill-opacity": [
                "case", ["boolean", ["feature-state", "hover"], false],
                0.1, ["boolean", ["feature-state", "selected"], false],
                0.0,
                0
            ],
            "fill-color": "red"
        },
        minzoom: 14,
        maxzoom: 17
    },
    {
        id: "sectors",
        name: "Sectors",
        checked: true,
        switcher: true,
        aois: [
            "el-pozon",
            "neiva",
            "brena",
            "chacarita",
            "tacumbu",
            "juchitan",
            "salina-cruz",
            "padang",
            "independencia"
        ],
        source: sources["sectors"],
        "source-layer": "default",
        type: "fill",
        layout: {
            visibility: "visible"
        },
        paint: {
            "fill-outline-color": "red",
            "fill-opacity": [
                "case", ["boolean", ["feature-state", "hover"], false],
                0.5, ["boolean", ["feature-state", "selected"], false],
                0.0,
                0
            ],
            "fill-color": "#EC90BC"
        },
        // paint: {
        //   "fill-outline-color": "black",
        //   "fill-opacity": [
        //     "case",
        //     ["boolean", ["feature-state", "hover"], false],
        //     0.7,
        //     ["boolean", ["feature-state", "selected"], false],
        //     0.9,
        //     0.0
        //   ],
        //   "fill-color": [
        //     "case",
        //     ["boolean", ["feature-state", "selected"], false],
        //     "#EC90BC",
        //     "#EC90BC"
        //   ]
        // },
        minzoom: 15,
        maxzoom: 17
    },
    {
        id: "greenspaces",
        name: "Greenspace",
        checked: true,
        switcher: true,
        aois: [
            "el-pozon",
            "neiva",
            "brena",
            "chacarita",
            "tacumbu",
            "juchitan",
            "salina-cruz",
            "padang",
            "independencia"
        ],
        source: sources["greenspace"],
        "source-layer": "default",
        type: "fill",
        paint: {
            "fill-outline-color": "black",
            "fill-opacity": [
                "case", ["boolean", ["feature-state", "hover"], false],
                0.7, ["boolean", ["feature-state", "selected"], false],
                0.7,
                0.9
            ],
            "fill-color": "#AAE08F"
        },
        layout: {
            visibility: "visible"
        },
        minzoom: 14,
        maxzoom: 21
    },

    {
        id: "sector-outlines",
        name: "Sector Outlines",
        checked: true,
        switcher: false,
        aois: [
            "el-pozon",
            "neiva",
            "brena",
            "chacarita",
            "tacumbu",
            "juchitan",
            "salina-cruz",
            "padang",
            "independencia"
        ],
        source: sources["sectors"],
        "source-layer": "default",
        type: "line",
        layout: {
            visibility: "visible"
        },
        paint: {
            "line-color": [
                "case", ["boolean", ["feature-state", "selected"], false],
                "#323232",
                "#323232"
            ],
            "line-opacity": [
                "case", ["boolean", ["feature-state", "selected"], false],
                1,
                1
            ],
            "line-width": 2
                // "line-dasharray": [2, 4]
        },
        minzoom: 15,
        maxzoom: 17
    },
    {
        id: "aoi-outline",
        name: "Area of Interest Outline",
        checked: true,
        switcher: false,
        aois: [
            "el-pozon",
            "neiva",
            "brena",
            "chacarita",
            "tacumbu",
            "juchitan",
            "salina-cruz",
            "padang",
            "independencia"
        ],
        source: sources["aoi"],
        "source-layer": "default",
        type: "line",
        paint: {
            "line-color": "red",
            "line-opacity": 1,
            "line-width": {
                stops: [
                    [10, 2],
                    [15, 3]
                ]
            }
        },
        layout: {
            visibility: "visible"
        },
        minzoom: 14,
        maxzoom: 17
    },
    {
        id: "drone-cover",
        name: "Drone Imagery",
        checked: true,
        switcher: true,
        aois: [
            "el-pozon",
            "neiva",
            "brena",
            "chacarita",
            "tacumbu",
            "juchitan",
            "salina-cruz",
            "padang",
            "independencia"
        ],
        source: {
            type: "raster",
            tiles: [DRONE_DOMAIN + "/api/geodata/drone/{aoi}/{z}/{x}/{y}.png"],
            tileSize: 256
        },
        type: "raster",
        paint: {},
        layout: {
            visibility: "visible"
        },
        minzoom: 17,
        maxzoom: 22
    },

    {
        id: "buildings",
        name: "Buildings",
        checked: true,
        switcher: true,
        aois: [
            "el-pozon",
            "neiva",
            "brena",
            "chacarita",
            "tacumbu",
            "juchitan",
            "salina-cruz",
            "padang",
            "independencia"
        ],
        source: sources["buildings"],
        "source-layer": "default",
        type: "fill",
        layout: {
            visibility: "none"
        },
        paint: {
            "fill-outline-color": "#2F4F4F",
            "fill-opacity": [
                "case", ["boolean", ["feature-state", "hover"], false],
                1, ["boolean", ["feature-state", "selected"], false],
                0.6,
                0.6
            ],
            "fill-color": [
                "case", ["boolean", ["feature-state", "selected"], false],
                "#EB2399",
                "#0D9AD0"
            ]
        },
        minzoom: 18,
        maxzoom: 21
    },
    {
        id: "building-outlines",
        name: "Building Outlines",
        checked: true,
        switcher: false,
        aois: [
            "el-pozon",
            "neiva",
            "brena",
            "chacarita",
            "tacumbu",
            "juchitan",
            "salina-cruz",
            "padang",
            "independencia"
        ],
        source: sources["buildings"],
        "source-layer": "default",
        type: "line",
        layout: {
            visibility: "none"
        },
        paint: {
            "line-color": [
                "case", ["boolean", ["feature-state", "selected"], false],
                "#EB2399",
                "#2F4F4F"
            ],
            "line-opacity": [
                "case", ["boolean", ["feature-state", "selected"], false],
                0.6,
                0.6
            ]
        },
        minzoom: 18,
        maxzoom: 21
    },
    {
        id: "sector-labels",
        checked: true,
        switcher: false,
        aois: [
            "el-pozon",
            "neiva",
            "brena",
            "chacarita",
            "tacumbu",
            "juchitan",
            "salina-cruz",
            "padang",
            "independencia"
        ],
        source: sources["sector-labels"],
        type: "symbol",
        layout: {
            visibility: "visible",
            "text-field": ["get", "name"]
        },
        paint: {
            "text-color": "white",
            "text-color": "hsl(0, 0%, 0%)",
            "text-halo-blur": 1,
            "text-halo-width": 1,
            "text-halo-color": "hsl(0, 0%, 100%)"
        },
        minzoom: 15,
        maxzoom: 18
    },

    {
        id: "drone-road-labels",
        name: "Drone Road Labels",
        checked: true,
        switcher: false,
        aois: [
            "el-pozon",
            "neiva",
            "brena",
            "chacarita",
            "tacumbu",
            "juchitan",
            "salina-cruz",
            "padang",
            "independencia"
        ],
        source: "composite",
        "source-layer": "road",
        type: "symbol",
        layout: {
            "symbol-placement": "line",
            "text-field": ["coalesce", ["get", "name_en"],
                ["get", "name"]
            ],
            "text-font": ["DIN Offc Pro Regular", "Arial Unicode MS Regular"],
            "text-letter-spacing": 0.01,
            "text-padding": 1,
            "text-pitch-alignment": "viewport",
            "text-rotation-alignment": "map"
        },
        paint: {
            "text-color": "hsl(0, 0%, 0%)",
            "text-halo-blur": 1,
            "text-halo-width": 1,
            "text-halo-color": [
                "match", ["get", "class"],
                ["motorway", "trunk"],
                "hsla(0, 0%, 100%, 0.75)",
                "hsl(0, 0%, 100%)"
            ]
        },
        minzoom: 17,
        maxzoom: 21
    },
    {
        id: "mapillary-sequences",
        name: "Mapillary",
        checked: false,
        switcher: false,
        aois: [
            "el-pozon",
            "neiva",
            "brena",
            "chacarita",
            "tacumbu",
            "juchitan",
            "salina-cruz",
            "padang",
            "independencia"
        ],
        type: "line",
        source: sources["mapillary"],
        "source-layer": "mapillary-sequences",
        layout: {
            "line-cap": "round",
            "line-join": "round"
        },
        paint: {
            "line-opacity": 0.6,
            "line-color": "rgb(53, 175, 109)",
            "line-width": 2
        },
        minzoom: 17,
        maxzoom: 20
    },
    {
        id: "mapillary-images",
        name: "Street View Coverage",
        checked: false,
        switcher: true,
        aois: [
            "el-pozon",
            "neiva",
            "brena",
            "chacarita",
            "tacumbu",
            "juchitan",
            "salina-cruz",
            "padang",
            "independencia"
        ],
        type: "circle",
        source: sources["mapillary"],
        "source-layer": "mapillary-images",
        paint: {
            "circle-color": "green",
            "circle-radius": 5
        },
        minzoom: 18,
        maxzoom: 20
    }
];

export const baseLayers = [{
    name: "Default",
    id: "default",
    style: "mapbox://styles/mapbox/streets-v11"
        // style: "mapbox://styles/santos1/ckkgmoqpx0ill17low8gafxqg"
}];