export const propertyFilters = [
  {
    id: "resettlement",
    prop: "dem_reset",
    value: "yes",
    title: "Resettlement",
    desc: `<p>Demand for resettlement: <strong>yes</strong>, if any hazard=5; total quality=poor or very poor. Otherwise, <strong>no</strong>. This is for illustrative purposes.</p>`,
    resultProp: "resettle",
    percentProp: "per_resettle",
    color: "#0D9AD0",
    expression: ["match", ["get", "dem_reset"], "yes", true, false]
  },
  {
    id: "softstory",
    prop: "soft_story",
    value: "yes",
    title: "Soft story",
    desc: `<p>Is this a potential soft story building? <strong>yes</strong> or <strong>no</strong>.
     For example, the building is at least 7.5 meters AND has at least one garage AND at least two windows. Other soft story calculations are possible.</p>`,
    resultProp: "softstory",
    percentProp: "per_softstory",
    color: "#0D9AD0",
    expression: ["match", ["get", "soft_story"], "yes", true, false]
  },
  {
    id: "public-land",
    prop: "land_publi",
    value: 1,
    title: "Public land",
    desc: `<p>Is the building on public land?</p>`,
    resultProp: "public_count",
    percentProp: "per_public",
    color: "#0D9AD0",
    expression: ["match", ["get", "land_publi"], 1, true, false]
  }
];

export const qualityFilters = [
  {
    id: "very-poor-condition",
    prop: "tot_qualit",
    value: "very poor",
    title: "Very Poor",
    desc: `If both roof and wall quality are poor.`,
    resultProp: "very_poor_count",
    percentProp: "very_poor",
    color: "#fa0000",
    expression: ["match", ["get", "tot_qualit"], "very poor", true, false]
  },
  {
    id: "poor-condition",
    prop: "tot_qualit",
    value: "poor",
    title: "Poor",
    desc: `If roof or wall quality is poor and the other is good, fair, under construction, vacant or otherwise unknown.`,
    resultProp: "poor_count",
    percentProp: "poor",
    color: "#f26521",
    expression: ["match", ["get", "tot_qualit"], "poor", true, false]
  },
  {
    id: "fair-condition",
    prop: "tot_qualit",
    value: "fair",
    title: "Fair",
    desc: `If both roof and wall quality are fair; or if one is fair and the other is good or under construction, vacant or otherwise unknown.`,
    resultProp: "fair_count",
    percentProp: "fair",
    color: "#f7941c",
    expression: ["match", ["get", "tot_qualit"], "fair", true, false]
  },
  {
    id: "good-condition",
    prop: "tot_qualit",
    value: "good",
    title: "Good",
    desc: `If roof or wall quality is good and the other is under construction, vacant or otherwise unknown.`,
    resultProp: "good_count",
    percentProp: "good",
    color: "#91a23d",
    expression: ["match", ["get", "tot_qualit"], "good", true, false]
  },
  {
    id: "very-good-condition",
    prop: "tot_qualit",
    value: "very good",
    title: "Very Good",
    desc: `If both roof and wall quality are good.`,
    resultProp: "very_good_count",
    percentProp: "very_good",
    color: "#008c50",
    expression: ["match", ["get", "tot_qualit"], "very good", true, false]
  }
];

export const useFilters = [
  {
    id: "residential",
    prop: "sv_use",
    value: "residential",
    title: "Residential",
    desc: `<p>The building is used solely for residential purposes.</p>`,
    resultProp: "residential_count",
    percentProp: "per_residential",
    color: "#1b9e77",
    expression: ["match", ["get", "sv_use"], "residential", true, false]
  },
  {
    id: "non-residential",
    prop: "sv_use",
    value: "non_residential",
    title: `Non-Residential`,
    desc: `<p>The building is used for commercial or public purposes. Examples include a government facility, school, hospital, church, market, bank or store.</p>`,
    resultProp: "commercial_count",
    percentProp: "per_commercial",
    color: "#d95f02",
    expression: [
      "any",
      ["match", ["get", "sv_use"], "non_residential", true, false],
      ["match", ["get", "sv_use"], "critical_infrastructure", true, false]
    ]
  },
  {
    id: "mixed",
    prop: "sv_use",
    value: "mixed",
    title: "Mixed",
    desc: `<p>The building is used for commercial/public and residential purposes. A common case is a mini-market on the first floor and residential housing above.</p>`,
    resultProp: "mixed_count",
    percentProp: "per_mixed",
    color: "#7570b3",
    expression: ["match", ["get", "sv_use"], "mixed", true, false]
  },
  {
    id: "critical",
    prop: "sv_use",
    value: "critical_infrastructure",
    title: "Infrastructure",
    desc: `<p>The building is used for public purposes, such as education, government, public services, health care, religion, banks or other public infrastructures.</p>`,
    resultProp: "critical_count",
    percentProp: "per_critical",
    color: "purple",
    expression: [
      "match",
      ["get", "sv_use"],
      "critical_infrastructure",
      true,
      false
    ]
  },
  {
    id: "unknown",
    prop: "sv_use",
    value: "",
    title: "Unknown",
    desc: `<p>The building use has not been determined.</p>`,
    resultProp: "unknown_count",
    percentProp: "per_unknown",
    color: "grey",
    expression: ["match", ["get", "sv_use"], "", true, false]
  }
];

export const surveyFilters = [
  {
    id: "survey-overcrowding",
    prop: "hac",
    value: "1",
    title: "Overcrowded houses",
    desc: `<p>Identify houses that are overcrowded.</p>`,
    expression: ["match", ["id"], [0], true, false],
    count: 0
  },
  {
    id: "survey-no-water",
    prop: "agua_3",
    value: "1",
    title: "No water",
    desc: `<p>Indentifies all the houses that have access to water just in their plots or in public spaces, or that are sharing water wih neighbors.</p>`,
    expression: ["match", ["id"], [0], true, false],
    count: 0
  },
  {
    id: "survey-chronic-disease",
    prop: "ecronica",
    value: "1",
    title: "Houses with disease",
    desc: `<p>Identifies houses in wich there is at least one person with a chronic disease.</p>`,
    expression: ["match", ["id"], [0], true, false],
    count: 0
  },
  {
    id: "survey-basic-education",
    prop: "sin_eeb",
    value: "1",
    title: "Basic Education",
    desc: `<p>Identifies houses in wich there is at least one person who did not finish basic education.</p>`,
    expression: ["match", ["id"], [0], true, false],
    count: 0
  },
  {
    id: "survey-internet-freq",
    prop: "s_internet_frec",
    value: "1",
    title: "Infrequent internet",
    desc: `<p>Identifies houses where there is infrequent internet access.</p>`,
    expression: ["match", ["id"], [0], true, false],
    count: 0
  },
  {
    id: "survey-no-telephone",
    prop: "sin_telefono",
    value: "1",
    title: "No phone / computer",
    desc: `<p>Identifies houses where there is no access to at least one smartphone, tablet or computer.</p>`,
    expression: ["match", ["id"], [0], true, false],
    count: 0
  },
  {
    id: "survey-waste-burning",
    prop: "basuras",
    value: "1",
    title: "No trash removal",
    desc: `<p>Identifies houses where domestic waste is burned, buried or dumped in the immediate environment.</p>`,
    expression: ["match", ["id"], [0], true, false],
    count: 0
  },
  {
    id: "survey-no-sanitation",
    prop: "sanitario",
    value: "1",
    title: "No sewage",
    desc: `<p>Identifies houses where the sewage is discharged into simple or filtered holes in the ground or is direclty discharged into streams.</p>`,
    expression: ["match", ["id"], [0], true, false],
    count: 0
  }
];
