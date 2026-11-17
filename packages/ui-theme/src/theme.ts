/* Optional Mantine v7 projection of the bundled design tokens.
 * Tokens are a static snapshot; manually review both files together.
 */
import { createTheme, type MantineColorsTuple } from "@mantine/core";

export const SEED = "#1F6E6A";

const brand: MantineColorsTuple = [
  "#e8f6f4", "#cdebe8", "#a8deda", "#83d5cf", "#5bbfb9",
  "#3aa49e", "#166d68", "#105955", "#0b4b47", "#00201e",
];

const success: MantineColorsTuple = [
  "#e6f7ed", "#c6eed8", "#9fe0bd", "#8bd8ac", "#5cc08a",
  "#3fa771", "#2e6b4f", "#235540", "#1e4634", "#09341f",
];

const warning: MantineColorsTuple = [
  "#fff6e0", "#ffeec0", "#ffe3a0", "#f5c563", "#e0ab3c",
  "#c08f22", "#7a5900", "#604600", "#4a3a10", "#3f2e00",
];

const danger: MantineColorsTuple = [
  "#fdeceb", "#f9dedc", "#f2b8b5", "#eb9995", "#e07672",
  "#d04f49", "#b3261e", "#8f1d17", "#5b1a17", "#410e0b",
];

const info: MantineColorsTuple = [
  "#e8f1ff", "#d3e4ff", "#b5d2ff", "#9cc9ff", "#6aa8f0",
  "#3f88d8", "#15548b", "#10436f", "#1d3450", "#001c38",
];

export const MOTION = { micro: 120, standard: 180, overlay: 240 } as const;
export const CHART_PALETTE = [
  "#0072b2", "#e69f00", "#009e73", "#cc79a7",
  "#56b4e9", "#d55e00", "#f0e442", "#666666",
] as const;

export const theme = createTheme({
  colors: { brand, success, warning, danger, info },
  primaryColor: "brand",
  primaryShade: { light: 6, dark: 3 },
  fontFamily: "Roboto Flex, system-ui, -apple-system, sans-serif",
  fontFamilyMonospace: "JetBrains Mono, ui-monospace, monospace",
  fontSizes: { xs: "10px", sm: "12px", md: "13px", lg: "16px", xl: "22px" },
  headings: {
    fontWeight: "600",
    sizes: {
      h1: { fontSize: "32px", lineHeight: "1.15" },
      h2: { fontSize: "22px", lineHeight: "1.2" },
      h3: { fontSize: "16px", lineHeight: "1.3" },
      h4: { fontSize: "13px", lineHeight: "1.4" },
    },
  },
  spacing: { xs: "4px", sm: "8px", md: "16px", lg: "24px", xl: "32px" },
  radius: { xs: "4px", sm: "8px", md: "10px", lg: "12px", xl: "16px" },
  defaultRadius: "sm",
  components: {
    Button: {
      defaultProps: { size: "sm" },
      styles: { root: { minHeight: "40px", fontWeight: 500 } },
    },
    TextInput: { defaultProps: { size: "sm" } },
    Select: { defaultProps: { size: "sm" } },
    Table: { defaultProps: { horizontalSpacing: "md", verticalSpacing: "xs" } },
    Modal: {
      defaultProps: { radius: "lg", transitionProps: { duration: MOTION.overlay } },
    },
    Tooltip: { defaultProps: { transitionProps: { duration: MOTION.micro } } },
    Notification: { defaultProps: { radius: "md" } },
  },
  other: { seed: SEED, motion: MOTION, chartPalette: CHART_PALETTE },
});
