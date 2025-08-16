import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Alert,
  Paper,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import Plot from 'react-plotly.js';
import { format, subMonths } from 'date-fns';

import { apiService } from '../services/apiService';

interface DashboardData {
  sankey_diagram: {
    chart: any;
    summary: {
      total_income: number;
      total_expenses: number;
      net_amount: number;
    };
  };
  spending_pie_chart: {
    chart: any;
    data: Record<string, number>;
  };
  monthly_trends: {
    chart: any;
    data: Record<string, { income: number; expenses: number }>;
  };
  credit_card_usage: {
    chart: any;
    data: Record<string, number>;
  };
}

const Dashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dateRange, setDateRange] = useState<string>('last_3_months');
  const [startDate, setStartDate] = useState<Date | null>(subMonths(new Date(), 3));
  const [endDate, setEndDate] = useState<Date | null>(new Date());

  // Mock user ID - in real app this would come from authentication
  const userId = 'demo-user-123';

  useEffect(() => {
    loadDashboardData();
  }, [startDate, endDate]);

  const loadDashboardData = async () => {
    setLoading(true);
    setError(null);

    try {
      const params: any = { user_id: userId };
      
      if (startDate) {
        params.start_date = format(startDate, 'yyyy-MM-dd');
      }
      if (endDate) {
        params.end_date = format(endDate, 'yyyy-MM-dd');
      }

      const data = await apiService.getDashboardData(params);
      setDashboardData(data);
    } catch (err) {
      setError('Failed to load dashboard data. Please try again.');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDateRangeChange = (value: string) => {
    setDateRange(value);
    const now = new Date();
    
    switch (value) {
      case 'last_month':
        setStartDate(subMonths(now, 1));
        setEndDate(now);
        break;
      case 'last_3_months':
        setStartDate(subMonths(now, 3));
        setEndDate(now);
        break;
      case 'last_6_months':
        setStartDate(subMonths(now, 6));
        setEndDate(now);
        break;
      case 'last_year':
        setStartDate(subMonths(now, 12));
        setEndDate(now);
        break;
      case 'custom':
        // Keep current dates for custom range
        break;
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress size={60} />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Financial Dashboard
      </Typography>

      {/* Date Range Controls */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={4}>
            <FormControl fullWidth>
              <InputLabel>Date Range</InputLabel>
              <Select
                value={dateRange}
                label="Date Range"
                onChange={(e) => handleDateRangeChange(e.target.value)}
              >
                <MenuItem value="last_month">Last Month</MenuItem>
                <MenuItem value="last_3_months">Last 3 Months</MenuItem>
                <MenuItem value="last_6_months">Last 6 Months</MenuItem>
                <MenuItem value="last_year">Last Year</MenuItem>
                <MenuItem value="custom">Custom Range</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          {dateRange === 'custom' && (
            <>
              <Grid item xs={12} sm={4}>
                <DatePicker
                  label="Start Date"
                  value={startDate}
                  onChange={(date) => setStartDate(date)}
                  slotProps={{ textField: { fullWidth: true } }}
                />
              </Grid>
              <Grid item xs={12} sm={4}>
                <DatePicker
                  label="End Date"
                  value={endDate}
                  onChange={(date) => setEndDate(date)}
                  slotProps={{ textField: { fullWidth: true } }}
                />
              </Grid>
            </>
          )}
        </Grid>
      </Paper>

      {dashboardData && (
        <>
          {/* Summary Cards */}
          <Grid container spacing={3} sx={{ mb: 3 }}>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Total Income
                  </Typography>
                  <Typography variant="h5" color="success.main">
                    {formatCurrency(dashboardData.sankey_diagram.summary.total_income)}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Total Expenses
                  </Typography>
                  <Typography variant="h5" color="error.main">
                    {formatCurrency(dashboardData.sankey_diagram.summary.total_expenses)}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Net Amount
                  </Typography>
                  <Typography 
                    variant="h5" 
                    color={dashboardData.sankey_diagram.summary.net_amount >= 0 ? 'success.main' : 'error.main'}
                  >
                    {formatCurrency(dashboardData.sankey_diagram.summary.net_amount)}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Cash Flow Sankey Diagram */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Cash Flow Diagram
              </Typography>
              <Box sx={{ height: '600px', width: '100%' }}>
                <Plot
                  data={dashboardData.sankey_diagram.chart.data}
                  layout={{
                    ...dashboardData.sankey_diagram.chart.layout,
                    autosize: true,
                    margin: { l: 0, r: 0, t: 30, b: 0 },
                  }}
                  style={{ width: '100%', height: '100%' }}
                  useResizeHandler
                  config={{ responsive: true }}
                />
              </Box>
            </CardContent>
          </Card>

          {/* Charts Grid */}
          <Grid container spacing={3}>
            {/* Spending Pie Chart */}
            <Grid item xs={12} lg={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Spending by Category
                  </Typography>
                  <Box sx={{ height: '400px' }}>
                    <Plot
                      data={dashboardData.spending_pie_chart.chart.data}
                      layout={{
                        ...dashboardData.spending_pie_chart.chart.layout,
                        autosize: true,
                        margin: { l: 0, r: 0, t: 30, b: 0 },
                      }}
                      style={{ width: '100%', height: '100%' }}
                      useResizeHandler
                      config={{ responsive: true }}
                    />
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Credit Card Usage */}
            <Grid item xs={12} lg={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Credit Card Usage
                  </Typography>
                  <Box sx={{ height: '400px' }}>
                    <Plot
                      data={dashboardData.credit_card_usage.chart.data}
                      layout={{
                        ...dashboardData.credit_card_usage.chart.layout,
                        autosize: true,
                        margin: { l: 40, r: 0, t: 30, b: 40 },
                      }}
                      style={{ width: '100%', height: '100%' }}
                      useResizeHandler
                      config={{ responsive: true }}
                    />
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Monthly Trends */}
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Monthly Trends
                  </Typography>
                  <Box sx={{ height: '400px' }}>
                    <Plot
                      data={dashboardData.monthly_trends.chart.data}
                      layout={{
                        ...dashboardData.monthly_trends.chart.layout,
                        autosize: true,
                        margin: { l: 60, r: 20, t: 30, b: 60 },
                      }}
                      style={{ width: '100%', height: '100%' }}
                      useResizeHandler
                      config={{ responsive: true }}
                    />
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </>
      )}
    </Box>
  );
};

export default Dashboard;