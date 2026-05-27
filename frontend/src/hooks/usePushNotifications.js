import { useEffect, useState } from 'react';
import { api } from '../lib/api';

function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
  const raw = atob(base64);
  return Uint8Array.from([...raw].map((c) => c.charCodeAt(0)));
}

export function usePushNotifications() {
  const [permission, setPermission] = useState(Notification.permission);
  const [subscribed, setSubscribed] = useState(false);

  const subscribe = async () => {
    if (!('serviceWorker' in navigator) || !('PushManager' in window)) return;

    try {
      // Pedir permissão
      const perm = await Notification.requestPermission();
      setPermission(perm);
      if (perm !== 'granted') return;

      // Buscar chave pública VAPID do backend
      const { publicKey } = await api.get('/push/vapid-public-key').then((r) => r.data);
      if (!publicKey) return;

      const reg = await navigator.serviceWorker.ready;
      const existing = await reg.pushManager.getSubscription();
      if (existing) { setSubscribed(true); return; }

      const sub = await reg.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(publicKey),
      });

      const subJson = sub.toJSON();
      await api.post('/push/subscribe', {
        endpoint: subJson.endpoint,
        keys: subJson.keys,
      });

      setSubscribed(true);
    } catch (err) {
      console.warn('push_subscribe_error', err);
    }
  };

  // Tentar se inscrever silenciosamente se já tiver permissão
  useEffect(() => {
    if (permission === 'granted' && !subscribed) {
      subscribe();
    }
  }, []); // eslint-disable-line

  return { permission, subscribed, subscribe };
}
