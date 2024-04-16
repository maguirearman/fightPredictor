import { Card, CardActions, CardContent, CardMedia, Button, Typography } from '@mui/material';

function FighterCard({ fighter }) {
    return (
      <Card sx={{ maxWidth: 345, m: 2 }}>
        <CardMedia
          component="img"
          height="140"
          image={fighter.image} // Path to fighter image
          alt={fighter.name}
        />
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            {fighter.name}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {fighter.summary} {/* Fighter summary */}
          </Typography>
        </CardContent>
        <CardActions>
          <Button size="small">Learn More</Button>
        </CardActions>
      </Card>
    );
  }

export default FighterCard;