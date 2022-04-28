import numeral from "numeral";

const attr_values = {
  non_residential: [["_", "-"]],
  "mix-other-unclear": [[/-/g, "/"]],
  brick_or_concrete_block: [
    [/_/g, " "],
    ["-", "/"]
  ],
  wood_polished: [["_", " "]],
  unreinforced_masonry: [["_", " "]],
  reinforced_masonry: [["_", " "]],
  timber_wooden_frame: [[/_/g, " "]],
  "wood_crude-plank": [
    ["_", " -"],
    ["-", "/"]
  ],
  "confined_masonry-concrete_frame": [
    [/_/g, " "],
    ["-", " / "]
  ],
  critical_infrastructure: [["_", " "]],
  corrugated_metal: [["_", " "]],
  disaster_mitigation: [["_", " "]],
  complete: [["complete", "yes"]],
  incomplete: [["incomplete", "no"]],
  d_tile: [["d_", ""]],
  "d_tile-metal": [
    ["d_", " "],
    ["-metal", " "]
  ],
  "d_tile-clay": [
    ["d_", " "],
    ["-clay", " "]
  ],
  d_metal: [["d_", " "]],
  d_concrete: [["d_", " "]],
  d_mixed: [["d_", " "]],
  d_good: [["d_", " "]],
  d_fair: [["d_", " "]],
  d_poor: [["d_", " "]],
  d_vacant: [["d_", " "]],
  "d_under construction": [["d_", " "]],
  d_blurred: [["d_", " "]]
};

export const FormatMixin = {
  methods: {
    formatNumber(val) {
      if (val) {
        return numeral(val).format("0,0");
      }
      return "0";
    },
    formatFloat(val) {
      if (val) {
        return numeral(val).format("0,0.00");
      }
      return "0";
    },
    formatString(val) {
      if (val) {
        return val.replace(/_| - /g, " ");
      }
      return "";
    },
    formatAttribute(val) {
      if (val) {
        let formats = attr_values[val];
        if (formats) {
          for (let format of formats) {
            val = val.replace(format[0], format[1]);
          }
          return val;
        } else {
          return val;
        }
      }
      return "";
    },
    formatGreenspace(val) {
      if (val && val > 1000000) {
        let n = numeral(val / 1000000).format("0,0.00");
        return `${n} km<sup>2</sup>`;
      } else if (val) {
        let n = numeral(val).format("0,0");
        return `${n} m<sup>2</sup>`;
      }
      return "0 m<sup>2</sup>";
    },
    capitalize(val) {
      if (val) {
        val = val.toLowerCase();
        return val.replace(/\b\w/g, l => l.toUpperCase());
      }
    }
  }
};
