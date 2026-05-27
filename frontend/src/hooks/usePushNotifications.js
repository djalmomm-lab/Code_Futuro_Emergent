import { useEffect, useState, useCallback } from 'react';
import { api } from '../lib/api';

function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
  const raw = atob(base64);
  return Uint8Array.from([...raw].map((c) => c.charCodeAt(0)));
}

const supported = typeof window !== 'undefined'
  && 'serviceWorker' in navigator
  && 'PushManager' in window
  && 'Notification' in window;

export function usePushNotifications() {
  const [permission, setPermission] = useState(
    supported ? Notification.permission : 'unsupported'
  );
  const [subscribed, setSubscribed] = useState(false);
  const [loading, setLoading] = useState(false);

  /* ─── Verificar se já inscrito ao montar ──────────────────────────────── */
  useEffect(() => {
    if (!supported || Notification.permission !== 'granted') return;
    navigator.serviceWorker.ready.then(async (reg) => {
      const existing = await reg.pushManager.getSubscription();
      if (existing) setSubscribed(true);
    }).catch(() => {});
  }, []);

  /* ─── Inscrever ───────────────────────────────────────────────────────── */
  const subscribe = useCallback(async () => {
    if (!supported) return;
    setLoading(true);
    try {
      const perm = await Notification.requestPermission();
      setPermission(perm);
      if (perm !== 'granted') return;

      const { publicKey } = await api.get('/push/vapid-public-key').then((r) => r.data);
      if (!publicKey) return;

      const reg = await navigator.serviceWorker.ready;
      let sub = await reg.pushManager.getSubscription();

      if (!sub) {
        sub = await reg.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: urlBase64ToUint8Array(publicKey),
        });
      }

      const subJson = sub.toJSON();
      await api.post('/push/subscribe', {
        endpoint: subJson.endpoint,
        keys: subJson.keys,
      });

      setSubscribed(true);
    } catch (err) {
      console.warn('push_subscribe_error', err);
    } finally {
      setLoading(false);
    }
  }, []);

  /* ─── Cancelar inscrição ──────────────────────────────────────────────── */
  const unsubscribe = useCallback(async () => {
    if (!supported) return;
    setLoading(true);
    try {
      const reg = await navigator.serviceWorker.ready;
      const sub = await reg.pushManager.getSubscription();

      if (sub) {
        const subJson = sub.toJSON();
        // Avisar backend para remover do banco
        await api.delete('/push/subscribe', {
          data: { endpoint: subJson.endpoint, keys: subJson.keys },
        }).catch(() => {});
        await sub.unsubscribe();
      }

      setSubscribed(false);
    } catch (err) {
      console.warn('push_unsubscribe_error', err);
    } finally {
      setLoading(false);
    }
  }, []);

  return { permission, subscribed, loading, subscribe, unsubscribe, supported };
}
