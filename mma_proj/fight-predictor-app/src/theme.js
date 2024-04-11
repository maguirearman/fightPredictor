import { createTheme} from '@mui/material/styles';


const theme = createTheme({
  palette: {
    primary: {
      main: '#770000', // Blood red for primary actions
    },
    secondary: {
      main: '#808080', // Accent color
    },
  },
  typography: {
    fontFamily: [
      'Roboto', 'Helvetica', 'Arial', 'sans-serif', 'Sternbach'
    ].join(','),
    h1: {
      fontWeight: 500,
    },
    // Customize as needed
  },
});

export default theme;