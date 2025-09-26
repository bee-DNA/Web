"""
Mapbox GL JS 地圖配置檔案
包含地圖樣式、API 設定和預設參數
"""

# Mapbox 配置
MAPBOX_CONFIG = {
    # 預設 Mapbox Access Token (需要在 https://www.mapbox.com/ 申請)
    'ACCESS_TOKEN': 'pk.eyJ1IjoiYmVlLWRuYSIsImEiOiJjbWZ5MTlhOTkwZnF3MmxvbjkwN2RtM2Z4In0.yFiY2MNpWqaDINuLaz1e0w',
    
    # 預設地圖中心點 (台北)
    'DEFAULT_CENTER': {
        'longitude': 121.5654,
        'latitude': 25.0330
    },
    
    # 預設縮放等級
    'DEFAULT_ZOOM': 2,
    
    # 地圖樣式配置
    'STYLES': {
        'osm_bright': {
            'name': 'OpenStreetMap 明亮版',
            'description': '基於 OpenStreetMap 的免費地圖樣式',
            'requires_token': False,
            'style': {
                'version': 8,
                'sources': {
                    'osm': {
                        'type': 'raster',
                        'tiles': ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
                        'tileSize': 256,
                        'attribution': '© OpenStreetMap contributors'
                    }
                },
                'layers': [{
                    'id': 'osm',
                    'type': 'raster',
                    'source': 'osm'
                }]
            }
        },
        'osm_dark': {
            'name': 'OpenStreetMap 深色版',
            'description': '深色主題的 OpenStreetMap 樣式',
            'requires_token': False,
            'style': {
                'version': 8,
                'sources': {
                    'osm_dark': {
                        'type': 'raster',
                        'tiles': ['https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png'],
                        'tileSize': 256,
                        'attribution': '© OpenStreetMap contributors, © CartoDB'
                    }
                },
                'layers': [{
                    'id': 'osm_dark',
                    'type': 'raster',
                    'source': 'osm_dark'
                }]
            }
        },
        'carto_positron': {
            'name': 'CartoDB Positron',
            'description': '簡約明亮的 CartoDB 樣式',
            'requires_token': False,
            'style': {
                'version': 8,
                'sources': {
                    'carto_positron': {
                        'type': 'raster',
                        'tiles': ['https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png'],
                        'tileSize': 256,
                        'attribution': '© OpenStreetMap contributors, © CartoDB'
                    }
                },
                'layers': [{
                    'id': 'carto_positron',
                    'type': 'raster',
                    'source': 'carto_positron'
                }]
            }
        },
        'mapbox_streets': {
            'name': 'Mapbox Streets',
            'description': 'Mapbox 官方街道樣式',
            'requires_token': True,
            'style_url': 'mapbox://styles/mapbox/streets-v12'
        },
        'mapbox_satellite': {
            'name': 'Mapbox 衛星圖',
            'description': '高解析度衛星影像',
            'requires_token': True,
            'style_url': 'mapbox://styles/mapbox/satellite-v9'
        },
        'mapbox_satellite_streets': {
            'name': 'Mapbox 衛星街道圖',
            'description': '衛星影像加上街道標籤',
            'requires_token': True,
            'style_url': 'mapbox://styles/mapbox/satellite-streets-v12'
        }
    }
}

# 圖層配置
LAYER_CONFIG = {
    'cities': {
        'name': '城市標記',
        'type': 'circle',
        'default_visible': True,
        'paint': {
            'circle-radius': [
                'interpolate',
                ['linear'],
                ['get', 'value'],
                0, 5,
                100, 20
            ],
            'circle-color': [
                'interpolate',
                ['linear'],
                ['get', 'value'],
                0, '#3498db',
                50, '#f39c12',
                80, '#e74c3c',
                100, '#9b59b6'
            ],
            'circle-opacity': 0.8,
            'circle-stroke-width': 2,
            'circle-stroke-color': '#ffffff'
        }
    },
    'heatmap': {
        'name': '熱力圖',
        'type': 'heatmap',
        'default_visible': False,
        'paint': {
            'heatmap-weight': [
                'interpolate',
                ['linear'],
                ['get', 'value'],
                0, 0,
                100, 1
            ],
            'heatmap-intensity': 0.7,
            'heatmap-radius': 50,
            'heatmap-opacity': 0.8
        }
    },
    'clusters': {
        'name': '聚類分析',
        'type': 'cluster',
        'default_visible': False,
        'cluster_options': {
            'cluster': True,
            'clusterMaxZoom': 14,
            'clusterRadius': 50
        },
        'paint': {
            'circle-color': '#e74c3c',
            'circle-radius': [
                'step',
                ['get', 'point_count'],
                20,
                100,
                30,
                750,
                40
            ],
            'circle-opacity': 0.7
        }
    }
}

# 資料配置
DATA_CONFIG = {
    'sample_data_file': 'sample_geographic_data.csv',
    'api_endpoints': {
        'cities': '/api/cities',
        'geojson': '/api/cities/geojson',
        'heatmap': '/api/heatmap',
        'statistics': '/api/statistics'
    },
    'supported_formats': ['csv', 'json', 'geojson'],
    'max_upload_size': 10 * 1024 * 1024,  # 10MB
}

# UI 配置
UI_CONFIG = {
    'sidebar_width': 350,
    'colors': {
        'primary': '#3498db',
        'success': '#27ae60',
        'warning': '#f39c12',
        'danger': '#e74c3c',
        'info': '#17a2b8',
        'light': '#f8f9fa',
        'dark': '#343a40'
    },
    'animations': {
        'transition_duration': '0.3s',
        'hover_transform': 'translateY(-2px)'
    }
}

# 效能配置
PERFORMANCE_CONFIG = {
    'max_points_for_labels': 100,  # 超過此數量時隱藏標籤
    'cluster_threshold': 500,      # 超過此數量時自動啟用聚類
    'heatmap_threshold': 1000,     # 超過此數量時建議使用熱力圖
    'tile_cache_size': 256,        # 地圖瓦片快取大小 (MB)
}

# 匯出所有配置
CONFIG = {
    'mapbox': MAPBOX_CONFIG,
    'layers': LAYER_CONFIG,
    'data': DATA_CONFIG,
    'ui': UI_CONFIG,
    'performance': PERFORMANCE_CONFIG
}