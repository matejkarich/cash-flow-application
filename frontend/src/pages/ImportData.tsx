import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  TextField,
  Alert,
  Paper,
  List,
  ListItem,
  ListItemText,
  Chip,
  CircularProgress,
} from '@mui/material';
import { Upload as UploadIcon, Google as GoogleIcon, Download as DownloadIcon } from '@mui/icons-material';
import { useDropzone } from 'react-dropzone';

import { apiService } from '../services/apiService';

const ImportData: React.FC = () => {
  const [googleSheetsId, setGoogleSheetsId] = useState('');
  const [googleSheetsRange, setGoogleSheetsRange] = useState('Sheet1');
  const [loading, setLoading] = useState(false);
  const [importResult, setImportResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  // Mock user ID
  const userId = 'demo-user-123';

  const onDrop = async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setLoading(true);
    setError(null);
    setImportResult(null);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('user_id', userId);

      const result = await apiService.importFromCSV(formData);
      setImportResult(result);
    } catch (err) {
      setError('Failed to import CSV file. Please check the format and try again.');
      console.error('CSV import error:', err);
    } finally {
      setLoading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
    },
    multiple: false,
  });

  const handleGoogleSheetsImport = async () => {
    if (!googleSheetsId.trim()) {
      setError('Please enter a Google Sheets ID');
      return;
    }

    setLoading(true);
    setError(null);
    setImportResult(null);

    try {
      const formData = new FormData();
      formData.append('spreadsheet_id', googleSheetsId);
      formData.append('range_name', googleSheetsRange);
      formData.append('user_id', userId);

      const result = await apiService.importFromGoogleSheets(formData);
      setImportResult(result);
    } catch (err) {
      setError('Failed to import from Google Sheets. Please check the ID and permissions.');
      console.error('Google Sheets import error:', err);
    } finally {
      setLoading(false);
    }
  };

  const downloadTemplate = async () => {
    try {
      const template = await apiService.getCSVTemplate();
      
      // Create and download the CSV file
      const blob = new Blob([template.content], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', template.filename);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('Failed to download template');
      console.error('Template download error:', err);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Import Financial Data
      </Typography>

      <Grid container spacing={3}>
        {/* CSV Upload */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Upload CSV File
              </Typography>
              <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                Upload a CSV file with your transaction data
              </Typography>

              <Paper
                {...getRootProps()}
                sx={{
                  p: 3,
                  border: '2px dashed',
                  borderColor: isDragActive ? 'primary.main' : 'grey.300',
                  bgcolor: isDragActive ? 'primary.light' + '10' : 'background.paper',
                  cursor: 'pointer',
                  textAlign: 'center',
                  mb: 2,
                }}
              >
                <input {...getInputProps()} />
                <UploadIcon sx={{ fontSize: 48, color: 'grey.400', mb: 1 }} />
                <Typography variant="h6" gutterBottom>
                  {isDragActive ? 'Drop the file here' : 'Drag & drop a CSV file'}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  or click to select a file
                </Typography>
              </Paper>

              <Button
                variant="outlined"
                startIcon={<DownloadIcon />}
                onClick={downloadTemplate}
                fullWidth
              >
                Download CSV Template
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* Google Sheets Import */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Import from Google Sheets
              </Typography>
              <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                Import data directly from a Google Sheets document
              </Typography>

              <TextField
                fullWidth
                label="Google Sheets ID"
                value={googleSheetsId}
                onChange={(e) => setGoogleSheetsId(e.target.value)}
                placeholder="1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
                sx={{ mb: 2 }}
                helperText="Found in the URL of your Google Sheets document"
              />

              <TextField
                fullWidth
                label="Range (optional)"
                value={googleSheetsRange}
                onChange={(e) => setGoogleSheetsRange(e.target.value)}
                placeholder="Sheet1"
                sx={{ mb: 2 }}
                helperText="Specify the sheet name or range (e.g., 'Sheet1' or 'A1:F100')"
              />

              <Button
                variant="contained"
                startIcon={<GoogleIcon />}
                onClick={handleGoogleSheetsImport}
                fullWidth
                disabled={loading}
              >
                Import from Google Sheets
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* Import Instructions */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Import Format Requirements
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" gutterBottom>
                    Required Columns:
                  </Typography>
                  <List dense>
                    <ListItem>
                      <ListItemText 
                        primary="Date" 
                        secondary="Format: YYYY-MM-DD, MM/DD/YYYY, or similar"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText 
                        primary="Amount" 
                        secondary="Negative for expenses, positive for income"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText 
                        primary="Description" 
                        secondary="Transaction description or merchant name"
                      />
                    </ListItem>
                  </List>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" gutterBottom>
                    Optional Columns:
                  </Typography>
                  <List dense>
                    <ListItem>
                      <ListItemText 
                        primary="Category" 
                        secondary="Main spending category"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText 
                        primary="Subcategory" 
                        secondary="More specific categorization"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText 
                        primary="Payment Method" 
                        secondary="Credit card, cash, debit, etc."
                      />
                    </ListItem>
                  </List>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Results */}
        {loading && (
          <Grid item xs={12}>
            <Box display="flex" justifyContent="center" alignItems="center" py={4}>
              <CircularProgress />
              <Typography sx={{ ml: 2 }}>Processing import...</Typography>
            </Box>
          </Grid>
        )}

        {error && (
          <Grid item xs={12}>
            <Alert severity="error" onClose={() => setError(null)}>
              {error}
            </Alert>
          </Grid>
        )}

        {importResult && (
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Import Results
                </Typography>
                <Box sx={{ mb: 2 }}>
                  <Chip 
                    label={`${importResult.transaction_count} transactions found`} 
                    color="success" 
                    sx={{ mr: 1 }}
                  />
                  {importResult.filename && (
                    <Chip 
                      label={`File: ${importResult.filename}`} 
                      variant="outlined" 
                    />
                  )}
                </Box>
                
                <Typography variant="subtitle2" gutterBottom>
                  Preview (first 5 transactions):
                </Typography>
                <Box sx={{ maxHeight: 300, overflow: 'auto' }}>
                  {importResult.preview.map((transaction: any, index: number) => (
                    <Paper key={index} sx={{ p: 2, mb: 1 }}>
                      <Grid container spacing={2}>
                        <Grid item xs={3}>
                          <Typography variant="body2">
                            <strong>Date:</strong> {transaction.date}
                          </Typography>
                        </Grid>
                        <Grid item xs={3}>
                          <Typography variant="body2">
                            <strong>Amount:</strong> ${transaction.amount}
                          </Typography>
                        </Grid>
                        <Grid item xs={4}>
                          <Typography variant="body2">
                            <strong>Description:</strong> {transaction.description}
                          </Typography>
                        </Grid>
                        <Grid item xs={2}>
                          <Typography variant="body2">
                            <strong>Method:</strong> {transaction.payment_method || 'N/A'}
                          </Typography>
                        </Grid>
                      </Grid>
                    </Paper>
                  ))}
                </Box>
                
                <Alert severity="success" sx={{ mt: 2 }}>
                  {importResult.message}
                </Alert>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default ImportData;