// FighterCard.js
import React from 'react';
import { Card, CardMedia, CardContent, Typography } from '@mui/material';

function FighterCard({ fighter }) {
  return (
    <Card sx={{ maxWidth: 345, m: 2 }}>
      <CardMedia
        component="img"
        height="140"
        image={fighter.image} // Ensure you have a URL to the fighter's image
        alt={fighter.name}
      />
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          {fighter.name}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Ranking: {fighter.ranking} {/* Example additional info */}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Weight Class: {fighter.weightClass} {/* More info */}
        </Typography>
      </CardContent>
    </Card>
  );
}

export default FighterCard;
