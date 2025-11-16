import { createI18n } from 'vue-i18n';
import enUS from '@/locales/en-US';
import ruRU from '@/locales/ru-RU';
import srSR from '@/locales/sr-SR';

const i18n = createI18n({
  locale: 'en',
  messages: {
    'en': enUS,
    'ru': ruRU,
    'sr': srSR
  }
});
export default i18n;