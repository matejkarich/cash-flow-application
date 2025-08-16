import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const Categories: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Categories
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            Category management functionality will be implemented here. This will include:
          </Typography>
          <ul>
            <li>Create and edit spending categories</li>
            <li>Set up hierarchical category structures (parent/child)</li>
            <li>Assign colors and icons to categories</li>
            <li>Set budget limits for categories</li>
            <li>Auto-categorization rules based on merchant names</li>
          </ul>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Categories;