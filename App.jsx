import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Bot, 
  Shield, 
  TrendingUp, 
  Zap, 
  BarChart3, 
  Settings, 
  FileText, 
  Github,
  Menu,
  X,
  ChevronRight,
  Star,
  Users,
  DollarSign,
  Activity,
  Target,
  Brain,
  Lock,
  Gauge,
  Wallet,
  AlertTriangle,
  CheckCircle,
  ArrowUpRight,
  Play,
  Download,
  ExternalLink
} from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area, BarChart, Bar } from 'recharts'
import './App.css'

// Mock data for charts
const performanceData = [
  { time: '00:00', profit: 0, trades: 0 },
  { time: '02:00', profit: 12.5, trades: 3 },
  { time: '04:00', profit: 28.3, trades: 7 },
  { time: '06:00', profit: 45.7, trades: 12 },
  { time: '08:00', profit: 62.1, trades: 18 },
  { time: '10:00', profit: 78.9, trades: 24 },
  { time: '12:00', profit: 95.4, trades: 31 },
]

const mevProtectionData = [
  { hour: '18:00', protected: 15, attacks: 3 },
  { hour: '19:00', protected: 23, attacks: 5 },
  { hour: '20:00', protected: 31, attacks: 7 },
  { hour: '21:00', protected: 28, attacks: 4 },
  { hour: '22:00', protected: 19, attacks: 2 },
]

// Navigation Component
const Navigation = () => {
  const [isOpen, setIsOpen] = useState(false)
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Home', icon: Bot },
    { path: '/dashboard', label: 'Dashboard', icon: BarChart3 },
    { path: '/features', label: 'Features', icon: Zap },
    { path: '/documentation', label: 'Docs', icon: FileText },
    { path: '/tools', label: 'Tools', icon: Settings },
  ]

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-xl">PumpBot Pro</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => {
              const Icon = item.icon
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    location.pathname === item.path
                      ? 'bg-primary text-primary-foreground'
                      : 'text-muted-foreground hover:text-foreground hover:bg-accent'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </Link>
              )
            })}
            <Button className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700">
              Get Started
            </Button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsOpen(!isOpen)}
            >
              {isOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        <AnimatePresence>
          {isOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="md:hidden border-t border-border"
            >
              <div className="px-2 pt-2 pb-3 space-y-1">
                {navItems.map((item) => {
                  const Icon = item.icon
                  return (
                    <Link
                      key={item.path}
                      to={item.path}
                      className={`flex items-center space-x-2 px-3 py-2 rounded-md text-base font-medium ${
                        location.pathname === item.path
                          ? 'bg-primary text-primary-foreground'
                          : 'text-muted-foreground hover:text-foreground hover:bg-accent'
                      }`}
                      onClick={() => setIsOpen(false)}
                    >
                      <Icon className="w-5 h-5" />
                      <span>{item.label}</span>
                    </Link>
                  )
                })}
                <div className="pt-2">
                  <Button className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700">
                    Get Started
                  </Button>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </nav>
  )
}

// Home Page Component
const HomePage = () => {
  const [currentFeature, setCurrentFeature] = useState(0)
  
  const features = [
    {
      icon: Shield,
      title: "MEV Protection",
      description: "Advanced front-running defense with 15-25% profit improvement",
      color: "from-green-500 to-emerald-600"
    },
    {
      icon: Brain,
      title: "AI Analysis",
      description: "Machine learning-enhanced token analysis and risk assessment",
      color: "from-blue-500 to-cyan-600"
    },
    {
      icon: Zap,
      title: "Lightning Execution",
      description: "Sub-second execution with optimal timing and slippage protection",
      color: "from-yellow-500 to-orange-600"
    },
    {
      icon: Target,
      title: "Pump.fun Optimized",
      description: "Platform-specific bonding curve analysis and migration timing",
      color: "from-purple-500 to-pink-600"
    }
  ]

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentFeature((prev) => (prev + 1) % features.length)
    }, 3000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <Badge className="mb-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white">
              🚀 Enhanced with MEV Protection & AI Analysis
            </Badge>
            <h1 className="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-600 via-purple-600 to-cyan-600 bg-clip-text text-transparent">
              Professional Pump.fun
              <br />
              Trading Bot
            </h1>
            <p className="text-xl text-muted-foreground mb-8 max-w-3xl mx-auto">
              Institutional-grade trading system with MEV protection, market microstructure analysis, 
              and AI-enhanced execution. Maximize gains while minimizing risks.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700">
                <Play className="w-5 h-5 mr-2" />
                Start Trading
              </Button>
              <Button size="lg" variant="outline">
                <Download className="w-5 h-5 mr-2" />
                Download Bot
              </Button>
            </div>
          </motion.div>

          {/* Performance Stats */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="mt-20 grid grid-cols-1 md:grid-cols-4 gap-6"
          >
            {[
              { label: "Profit Improvement", value: "+25%", icon: TrendingUp, color: "text-green-500" },
              { label: "MEV Protection", value: "95.2%", icon: Shield, color: "text-blue-500" },
              { label: "Success Rate", value: "87.4%", icon: Target, color: "text-purple-500" },
              { label: "Active Users", value: "2,847", icon: Users, color: "text-cyan-500" }
            ].map((stat, index) => (
              <Card key={index} className="text-center">
                <CardContent className="pt-6">
                  <stat.icon className={`w-8 h-8 mx-auto mb-2 ${stat.color}`} />
                  <div className="text-2xl font-bold">{stat.value}</div>
                  <div className="text-sm text-muted-foreground">{stat.label}</div>
                </CardContent>
              </Card>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features Showcase */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Advanced Trading Features
            </h2>
            <p className="text-xl text-muted-foreground">
              Professional-grade capabilities that give you the edge
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              {features.map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className={`p-6 rounded-lg border transition-all duration-300 cursor-pointer ${
                    currentFeature === index 
                      ? 'bg-card border-primary shadow-lg' 
                      : 'bg-card/50 hover:bg-card border-border'
                  }`}
                  onClick={() => setCurrentFeature(index)}
                >
                  <div className="flex items-center space-x-4">
                    <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${feature.color} flex items-center justify-center`}>
                      <feature.icon className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold">{feature.title}</h3>
                      <p className="text-muted-foreground">{feature.description}</p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>

            <div className="relative">
              <Card className="p-6">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Activity className="w-5 h-5" />
                    <span>Real-time Performance</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={performanceData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="time" />
                      <YAxis />
                      <Tooltip />
                      <Area 
                        type="monotone" 
                        dataKey="profit" 
                        stroke="#8884d8" 
                        fill="url(#colorProfit)" 
                      />
                      <defs>
                        <linearGradient id="colorProfit" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
                          <stop offset="95%" stopColor="#8884d8" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                    </AreaChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-3xl md:text-4xl font-bold mb-6">
              Ready to Start Trading?
            </h2>
            <p className="text-xl text-muted-foreground mb-8">
              Join thousands of traders using our advanced pump.fun bot
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700">
                <Github className="w-5 h-5 mr-2" />
                View on GitHub
              </Button>
              <Button size="lg" variant="outline">
                <FileText className="w-5 h-5 mr-2" />
                Read Documentation
              </Button>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}

// Dashboard Component
const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('overview')

  return (
    <div className="pt-20 px-4 sm:px-6 lg:px-8 min-h-screen">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Trading Dashboard</h1>
          <p className="text-muted-foreground">Monitor your bot's performance and market opportunities</p>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="performance">Performance</TabsTrigger>
            <TabsTrigger value="opportunities">Opportunities</TabsTrigger>
            <TabsTrigger value="settings">Settings</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {[
                { title: "Total Profit", value: "$12,847", change: "+23.5%", icon: DollarSign, color: "text-green-500" },
                { title: "Active Positions", value: "3", change: "2 profitable", icon: Wallet, color: "text-blue-500" },
                { title: "Success Rate", value: "87.4%", change: "+5.2%", icon: Target, color: "text-purple-500" },
                { title: "MEV Protected", value: "156", change: "15 attacks blocked", icon: Shield, color: "text-cyan-500" }
              ].map((metric, index) => (
                <Card key={index}>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-muted-foreground">{metric.title}</p>
                        <p className="text-2xl font-bold">{metric.value}</p>
                        <p className={`text-sm ${metric.color}`}>{metric.change}</p>
                      </div>
                      <metric.icon className={`w-8 h-8 ${metric.color}`} />
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Profit Over Time</CardTitle>
                  <CardDescription>24-hour performance tracking</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={performanceData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="time" />
                      <YAxis />
                      <Tooltip />
                      <Line type="monotone" dataKey="profit" stroke="#8884d8" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>MEV Protection</CardTitle>
                  <CardDescription>Attacks blocked vs transactions protected</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={mevProtectionData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="hour" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="protected" fill="#8884d8" />
                      <Bar dataKey="attacks" fill="#82ca9d" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="performance" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <Card className="lg:col-span-2">
                <CardHeader>
                  <CardTitle>Strategy Performance</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {[
                    { name: "Sniping Strategy", profit: 45.2, trades: 23, winRate: 91.3 },
                    { name: "Long-term Strategy", profit: 32.8, trades: 12, winRate: 83.3 },
                    { name: "Arbitrage Strategy", profit: 18.5, trades: 8, winRate: 75.0 }
                  ].map((strategy, index) => (
                    <div key={index} className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="font-medium">{strategy.name}</span>
                        <span className="text-green-500">+{strategy.profit}%</span>
                      </div>
                      <Progress value={strategy.winRate} className="h-2" />
                      <div className="flex justify-between text-sm text-muted-foreground">
                        <span>{strategy.trades} trades</span>
                        <span>{strategy.winRate}% win rate</span>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Risk Metrics</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {[
                    { label: "Max Drawdown", value: "8.2%", status: "good" },
                    { label: "Sharpe Ratio", value: "2.34", status: "excellent" },
                    { label: "Win Rate", value: "87.4%", status: "excellent" },
                    { label: "Avg Trade", value: "12.3%", status: "good" }
                  ].map((metric, index) => (
                    <div key={index} className="flex justify-between items-center">
                      <span className="text-sm">{metric.label}</span>
                      <div className="flex items-center space-x-2">
                        <span className="font-medium">{metric.value}</span>
                        <CheckCircle className={`w-4 h-4 ${
                          metric.status === 'excellent' ? 'text-green-500' : 'text-blue-500'
                        }`} />
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="opportunities" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Current Opportunities</CardTitle>
                <CardDescription>High-potential tokens identified by AI analysis</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    { name: "MOONSHOT", score: 8.7, risk: "Low", potential: "180%", recommendation: "Strong Buy" },
                    { name: "ROCKET", score: 8.2, risk: "Medium", potential: "150%", recommendation: "Buy" },
                    { name: "PUMP", score: 7.8, risk: "Low", potential: "120%", recommendation: "Consider" }
                  ].map((token, index) => (
                    <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-4">
                        <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold">
                          {token.name[0]}
                        </div>
                        <div>
                          <div className="font-medium">{token.name}</div>
                          <div className="text-sm text-muted-foreground">Score: {token.score}/10</div>
                        </div>
                      </div>
                      <div className="text-right space-y-1">
                        <Badge variant={token.risk === 'Low' ? 'default' : 'secondary'}>
                          {token.risk} Risk
                        </Badge>
                        <div className="text-sm text-green-500">+{token.potential}</div>
                        <div className="text-xs text-muted-foreground">{token.recommendation}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="settings" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Trading Settings</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Risk per Trade</label>
                    <div className="flex items-center space-x-2">
                      <Progress value={20} className="flex-1" />
                      <span className="text-sm">2%</span>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Max Positions</label>
                    <div className="flex items-center space-x-2">
                      <Progress value={60} className="flex-1" />
                      <span className="text-sm">3</span>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Stop Loss</label>
                    <div className="flex items-center space-x-2">
                      <Progress value={75} className="flex-1" />
                      <span className="text-sm">15%</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>System Status</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {[
                    { component: "MEV Protection", status: "Active", color: "text-green-500" },
                    { component: "Market Analyzer", status: "Running", color: "text-green-500" },
                    { component: "Strategy Engine", status: "Active", color: "text-green-500" },
                    { component: "Risk Manager", status: "Monitoring", color: "text-blue-500" }
                  ].map((item, index) => (
                    <div key={index} className="flex justify-between items-center">
                      <span className="text-sm">{item.component}</span>
                      <div className="flex items-center space-x-2">
                        <span className={`text-sm ${item.color}`}>{item.status}</span>
                        <div className={`w-2 h-2 rounded-full ${
                          item.color === 'text-green-500' ? 'bg-green-500' : 'bg-blue-500'
                        }`} />
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

// Features Page Component
const FeaturesPage = () => {
  const features = [
    {
      icon: Shield,
      title: "MEV Protection",
      description: "Advanced front-running defense with private mempool integration",
      benefits: [
        "15-25% profit improvement",
        "80% reduction in MEV attacks",
        "Private mempool routing",
        "Dynamic gas optimization"
      ],
      color: "from-green-500 to-emerald-600"
    },
    {
      icon: Brain,
      title: "AI-Enhanced Analysis",
      description: "Machine learning-powered token analysis and risk assessment",
      benefits: [
        "Real-time pattern recognition",
        "Developer credibility scoring",
        "Community sentiment analysis",
        "Predictive modeling"
      ],
      color: "from-blue-500 to-cyan-600"
    },
    {
      icon: Zap,
      title: "Lightning Execution",
      description: "Sub-second execution with optimal timing and slippage protection",
      benefits: [
        "Sub-second execution speed",
        "Intelligent order splitting",
        "Slippage minimization",
        "Optimal timing algorithms"
      ],
      color: "from-yellow-500 to-orange-600"
    },
    {
      icon: Target,
      title: "Pump.fun Optimization",
      description: "Platform-specific bonding curve analysis and migration timing",
      benefits: [
        "Bonding curve intelligence",
        "Migration timing optimization",
        "Platform momentum tracking",
        "Graduation probability scoring"
      ],
      color: "from-purple-500 to-pink-600"
    }
  ]

  return (
    <div className="pt-20 px-4 sm:px-6 lg:px-8 min-h-screen">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold mb-4">Advanced Features</h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Professional-grade trading capabilities that give you the competitive edge in pump.fun markets
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card className="h-full">
                <CardHeader>
                  <div className="flex items-center space-x-4">
                    <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${feature.color} flex items-center justify-center`}>
                      <feature.icon className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <CardTitle>{feature.title}</CardTitle>
                      <CardDescription>{feature.description}</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {feature.benefits.map((benefit, benefitIndex) => (
                      <li key={benefitIndex} className="flex items-center space-x-2">
                        <CheckCircle className="w-4 h-4 text-green-500" />
                        <span className="text-sm">{benefit}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Performance Comparison */}
        <section className="mt-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Performance Comparison</h2>
            <p className="text-muted-foreground">See how our enhanced features improve trading results</p>
          </div>

          <Card>
            <CardContent className="p-8">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {[
                  { metric: "Profit Improvement", before: "0%", after: "+25%", improvement: "25%" },
                  { metric: "MEV Protection", before: "0%", after: "95.2%", improvement: "95.2%" },
                  { metric: "Success Rate", before: "65%", after: "87.4%", improvement: "22.4%" }
                ].map((comparison, index) => (
                  <div key={index} className="text-center">
                    <h3 className="font-semibold mb-4">{comparison.metric}</h3>
                    <div className="space-y-2">
                      <div className="text-sm text-muted-foreground">Before</div>
                      <div className="text-2xl font-bold text-red-500">{comparison.before}</div>
                      <ArrowUpRight className="w-6 h-6 mx-auto text-green-500" />
                      <div className="text-sm text-muted-foreground">After</div>
                      <div className="text-2xl font-bold text-green-500">{comparison.after}</div>
                      <Badge className="bg-green-100 text-green-800">
                        +{comparison.improvement} improvement
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </section>
      </div>
    </div>
  )
}

// Documentation Page Component
const DocumentationPage = () => {
  const [activeSection, setActiveSection] = useState('getting-started')

  const sections = [
    { id: 'getting-started', title: 'Getting Started', icon: Play },
    { id: 'installation', title: 'Installation', icon: Download },
    { id: 'configuration', title: 'Configuration', icon: Settings },
    { id: 'strategies', title: 'Trading Strategies', icon: Target },
    { id: 'api', title: 'API Reference', icon: FileText },
    { id: 'troubleshooting', title: 'Troubleshooting', icon: AlertTriangle }
  ]

  return (
    <div className="pt-20 px-4 sm:px-6 lg:px-8 min-h-screen">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar */}
          <div className="lg:w-64 flex-shrink-0">
            <div className="sticky top-24">
              <h2 className="font-semibold mb-4">Documentation</h2>
              <nav className="space-y-1">
                {sections.map((section) => (
                  <button
                    key={section.id}
                    onClick={() => setActiveSection(section.id)}
                    className={`w-full flex items-center space-x-2 px-3 py-2 text-left rounded-md text-sm transition-colors ${
                      activeSection === section.id
                        ? 'bg-primary text-primary-foreground'
                        : 'text-muted-foreground hover:text-foreground hover:bg-accent'
                    }`}
                  >
                    <section.icon className="w-4 h-4" />
                    <span>{section.title}</span>
                  </button>
                ))}
              </nav>
            </div>
          </div>

          {/* Content */}
          <div className="flex-1">
            <Card>
              <CardContent className="p-8">
                {activeSection === 'getting-started' && (
                  <div className="space-y-6">
                    <h1 className="text-3xl font-bold">Getting Started</h1>
                    <p className="text-muted-foreground">
                      Welcome to the Pump.fun Trading Bot documentation. This guide will help you set up and start using the bot.
                    </p>
                    
                    <div className="space-y-4">
                      <h2 className="text-xl font-semibold">Quick Start</h2>
                      <ol className="list-decimal list-inside space-y-2 text-sm">
                        <li>Clone the repository from GitHub</li>
                        <li>Install dependencies with <code className="bg-muted px-2 py-1 rounded">pip install -r requirements.txt</code></li>
                        <li>Configure your environment variables</li>
                        <li>Run the bot with <code className="bg-muted px-2 py-1 rounded">python src/main.py</code></li>
                      </ol>
                    </div>

                    <div className="bg-muted p-4 rounded-lg">
                      <h3 className="font-semibold mb-2">⚠️ Important</h3>
                      <p className="text-sm">
                        Always start with small amounts and test thoroughly before deploying with larger capital.
                      </p>
                    </div>
                  </div>
                )}

                {activeSection === 'installation' && (
                  <div className="space-y-6">
                    <h1 className="text-3xl font-bold">Installation</h1>
                    
                    <div className="space-y-4">
                      <h2 className="text-xl font-semibold">System Requirements</h2>
                      <ul className="list-disc list-inside space-y-1 text-sm">
                        <li>Python 3.11 or higher</li>
                        <li>Node.js 18+ (for web interface)</li>
                        <li>4GB RAM minimum</li>
                        <li>Stable internet connection</li>
                      </ul>
                    </div>

                    <div className="space-y-4">
                      <h2 className="text-xl font-semibold">Installation Steps</h2>
                      <div className="bg-muted p-4 rounded-lg">
                        <pre className="text-sm">
{`# Clone the repository
git clone https://github.com/your-repo/pump-fun-bot.git
cd pump-fun-bot

# Install Python dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit configuration
nano .env`}
                        </pre>
                      </div>
                    </div>
                  </div>
                )}

                {activeSection === 'configuration' && (
                  <div className="space-y-6">
                    <h1 className="text-3xl font-bold">Configuration</h1>
                    
                    <div className="space-y-4">
                      <h2 className="text-xl font-semibold">Environment Variables</h2>
                      <div className="space-y-3">
                        {[
                          { key: 'PUMPPORTAL_API_KEY', description: 'Your PumpPortal API key for trading' },
                          { key: 'WALLET_PRIVATE_KEY', description: 'Private key for your trading wallet' },
                          { key: 'RISK_PER_TRADE', description: 'Risk percentage per trade (default: 0.02)' },
                          { key: 'ENABLE_MEV_PROTECTION', description: 'Enable MEV protection (default: true)' }
                        ].map((env, index) => (
                          <div key={index} className="border rounded-lg p-4">
                            <code className="font-mono text-sm bg-muted px-2 py-1 rounded">{env.key}</code>
                            <p className="text-sm text-muted-foreground mt-1">{env.description}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {/* Add more sections as needed */}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

// Tools Page Component
const ToolsPage = () => {
  return (
    <div className="pt-20 px-4 sm:px-6 lg:px-8 min-h-screen">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-3xl font-bold mb-4">Trading Tools</h1>
          <p className="text-muted-foreground">
            Interactive tools to help you analyze opportunities and optimize your trading
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            {
              title: "Opportunity Scanner",
              description: "Real-time scanning for high-potential tokens",
              icon: Target,
              color: "from-blue-500 to-cyan-600",
              features: ["AI-powered analysis", "Real-time alerts", "Risk assessment"]
            },
            {
              title: "Risk Calculator",
              description: "Calculate optimal position sizes and risk levels",
              icon: Gauge,
              color: "from-green-500 to-emerald-600",
              features: ["Position sizing", "Risk metrics", "Portfolio analysis"]
            },
            {
              title: "Market Analyzer",
              description: "Deep market microstructure analysis",
              icon: BarChart3,
              color: "from-purple-500 to-pink-600",
              features: ["Liquidity analysis", "Whale tracking", "Price prediction"]
            },
            {
              title: "Strategy Backtester",
              description: "Test your strategies against historical data",
              icon: Activity,
              color: "from-orange-500 to-red-600",
              features: ["Historical testing", "Performance metrics", "Strategy optimization"]
            },
            {
              title: "MEV Monitor",
              description: "Monitor MEV attacks and protection effectiveness",
              icon: Shield,
              color: "from-cyan-500 to-blue-600",
              features: ["Attack detection", "Protection stats", "Gas optimization"]
            },
            {
              title: "Portfolio Tracker",
              description: "Track your trading performance and metrics",
              icon: Wallet,
              color: "from-pink-500 to-purple-600",
              features: ["P&L tracking", "Performance analytics", "Risk monitoring"]
            }
          ].map((tool, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card className="h-full hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${tool.color} flex items-center justify-center mb-4`}>
                    <tool.icon className="w-6 h-6 text-white" />
                  </div>
                  <CardTitle>{tool.title}</CardTitle>
                  <CardDescription>{tool.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-1">
                    {tool.features.map((feature, featureIndex) => (
                      <li key={featureIndex} className="flex items-center space-x-2 text-sm">
                        <CheckCircle className="w-3 h-3 text-green-500" />
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>
                  <Button className="w-full mt-4" variant="outline">
                    Launch Tool
                    <ExternalLink className="w-4 h-4 ml-2" />
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  )
}

// Main App Component
function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background">
        <Navigation />
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/features" element={<FeaturesPage />} />
            <Route path="/documentation" element={<DocumentationPage />} />
            <Route path="/tools" element={<ToolsPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App

