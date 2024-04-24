// FighterCard.js
import React from 'react';
import { Card, CardMedia, CardContent, Typography, Box } from '@mui/material';

function FighterCard({ fighter }) {
  // Aspect ratio calculation based on original dimensions (460x700)
  const aspectRatio = (700 / 460) * 100; // Calculate the height as a percentage of the width


return (
    <Card sx={{ maxWidth: 250, m: 2, padding: 0 }}> 
        <Box sx={{ width: '100%', pt: `${aspectRatio}%`, position: 'relative' }}> 
            <CardMedia
                component="img"
                sx={{
                    position: 'absolute', // Absolutely position the image to cover the box
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover' // Cover ensures the image covers the box area, cropping if necessary
                }}
                image={fighter.image}
                alt={fighter.name}
            />
        </Box>
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
