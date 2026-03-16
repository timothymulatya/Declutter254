import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import StatusBadge from '../components/StatusBadge';
import { Gift, Handshake, Globe, Sparkles } from 'lucide-react';

const Dashboard = () => {
    const { user } = useAuth();
    const [stats, setStats] = useState(null);
    const [activity, setActivity] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                const [statsRes, activityRes] = await Promise.all([
                    axios.get('http://localhost:5555/api/dashboard/stats'),
                    axios.get('http://localhost:5555/api/dashboard/activity')
                ]);
                setStats(statsRes.data);
                setActivity(activityRes.data);
            } catch (error) {
                console.error('Error fetching dashboard data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchDashboardData();
    }, []);

    if (loading) {
        return (
            <div style={{ padding: '60px', textAlign: 'center' }}>
                <h2 style={{ color: 'var(--accent-maroon)' }}>Loading your dashboard...</h2>
            </div>
        );
    }

    return (
        <div style={{ padding: '40px 20px', maxWidth: '1200px', margin: '0 auto' }}>
            <header style={{ marginBottom: '40px' }}>
                <h1 style={{ fontSize: '2.4rem', color: 'var(--accent-maroon)', marginBottom: '8px' }}>
                    Welcome, {user?.name}
                </h1>
                <p style={{ color: '#666', fontSize: '1.1rem' }}>Here's what's happening with your items and requests.</p>
            </header>

            {/* Stats Overview */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                gap: '24px',
                marginBottom: '48px'
            }}>
                <StatCard
                    title="Items Given"
                    value={stats?.as_giver?.items_given || 0}
                    Icon={Gift}
                    iconColor="var(--accent-maroon)"
                />
                <StatCard
                    title="Items Received"
                    value={stats?.as_seeker?.items_received || 0}
                    Icon={Handshake}
                    iconColor="var(--primary-skyblue)"
                />
                <StatCard
                    title="Waste Prevented"
                    value={`${stats?.impact?.waste_prevented_kg || 0} kg`}
                    Icon={Globe}
                    iconColor="#10b981"
                />
                <StatCard
                    title="People Helped"
                    value={stats?.impact?.people_helped || 0}
                    Icon={Sparkles}
                    iconColor="#f59e0b"
                />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
                {/* As Giver Section */}
                <section style={sectionStyle}>
                    <h2 style={sectionTitleStyle}>Giver Activity</h2>
                    <div style={{ marginBottom: '20px' }}>
                        <p><strong>Available Items:</strong> {stats?.as_giver?.items_available || 0}</p>
                        <p><strong>Total Requests:</strong> {stats?.as_giver?.incoming_requests || 0}</p>
                    </div>
                    <div>
                        <h3 style={subTitleStyle}>Recent Incoming Requests</h3>
                        {activity?.incoming_requests?.length > 0 ? (
                            <ul style={listStyle}>
                                {activity.incoming_requests.map(req => (
                                    <li key={req.id} style={listItemStyle}>
                                        <div>
                                            <strong>{req.seeker_name}</strong> requested <strong>{req.item_title}</strong>
                                            <div style={{ fontSize: '0.85rem', color: '#888' }}>{new Date(req.created_at).toLocaleDateString()}</div>
                                        </div>
                                        <StatusBadge status={req.status} />
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p style={{ color: '#999', fontStyle: 'italic' }}>No recent requests on your items.</p>
                        )}
                    </div>
                </section>

                {/* As Seeker Section */}
                <section style={sectionStyle}>
                    <h2 style={sectionTitleStyle}>Seeker Activity</h2>
                    <div style={{ marginBottom: '20px' }}>
                        <p><strong>Outgoing Requests:</strong> {stats?.as_seeker?.outgoing_requests || 0}</p>
                        <p><strong>Approved:</strong> {stats?.as_seeker?.approved_requests || 0}</p>
                    </div>
                    <div>
                        <h3 style={subTitleStyle}>My Recent Requests</h3>
                        {activity?.outgoing_requests?.length > 0 ? (
                            <ul style={listStyle}>
                                {activity.outgoing_requests.map(req => (
                                    <li key={req.id} style={listItemStyle}>
                                        <div>
                                            Request for <strong>{req.item_title}</strong>
                                            <div style={{ fontSize: '0.85rem', color: '#888' }}>{new Date(req.created_at).toLocaleDateString()}</div>
                                        </div>
                                        <StatusBadge status={req.status} />
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p style={{ color: '#999', fontStyle: 'italic' }}>You haven't made any requests recently.</p>
                        )}
                    </div>
                </section>
            </div>
        </div>
    );
};

const StatCard = ({ title, value, Icon, iconColor }) => (
    <div style={{
        background: 'white',
        padding: '24px',
        borderRadius: '20px',
        boxShadow: '0 10px 30px rgba(0,0,0,0.05)',
        display: 'flex',
        alignItems: 'center',
        gap: '20px',
        border: '1px solid #f0f0f0'
    }}>
        <div style={{
            background: `${iconColor}15`,
            padding: '12px',
            borderRadius: '12px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
        }}>
            <Icon size={32} color={iconColor} />
        </div>
        <div>
            <div style={{ color: '#888', fontSize: '0.9rem', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.5px' }}>{title}</div>
            <div style={{ fontSize: '1.8rem', fontWeight: '800', color: 'var(--neutral-black)' }}>{value}</div>
        </div>
    </div>
);

const sectionStyle = {
    background: 'white',
    padding: '32px',
    borderRadius: '24px',
    boxShadow: '0 4px 20px rgba(0,0,0,0.03)',
    border: '1px solid #f0f0f0'
};

const sectionTitleStyle = {
    fontSize: '1.4rem',
    color: 'var(--accent-maroon)',
    marginBottom: '24px',
    borderBottom: '2px solid #f8f8f8',
    paddingBottom: '12px'
};

const subTitleStyle = {
    fontSize: '1rem',
    fontWeight: '700',
    marginBottom: '16px',
    color: '#444'
};

const listStyle = {
    listStyle: 'none',
    padding: 0,
    margin: 0
};

const listItemStyle = {
    padding: '16px 0',
    borderBottom: '1px solid #f5f5f5',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
};

export default Dashboard;
