export interface Transport {
  id: string;
  type: TransportType;
  line: string;
  origin: string;
  destination: string;
  departureTime: string;
  arrivalTime: string;
  status: TransportStatus;
  platform?: string;
  gate?: string;
  route?: string[];
  estimatedDelay?: number;
  statusMessage?: string;

  // ✅ Newly added fields for frontend display
  departureTimeFormatted?: string;
  arrivalTimeFormatted?: string;
}

export type TransportType = 'train' | 'bus' | 'tram' | 'ice';

export type TransportStatus = 'on-time' | 'delayed' | 'cancelled' | 'boarding';

export interface FilterState {
  train: boolean;
  bus: boolean;
  tram: boolean;
  ice: boolean;
}
