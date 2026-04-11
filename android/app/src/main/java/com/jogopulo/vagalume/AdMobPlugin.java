package com.jogopulo.vagalume;

import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.google.android.gms.ads.AdListener;
import com.google.android.gms.ads.AdRequest;
import com.google.android.gms.ads.AdSize;
import com.google.android.gms.ads.AdView;
import com.google.android.gms.ads.LoadAdError;
import com.google.android.gms.ads.MobileAds;

@CapacitorPlugin(name = "AdMob")
public class AdMobPlugin extends Plugin {

    private static final String TAG = "AdMobPlugin";
    private AdView bannerView;
    private static final String BANNER_AD_ID = "ca-app-pub-9818608541760893/7775498565";

    @Override
    public void load() {
        Log.d(TAG, "Inicializando Google Mobile Ads SDK...");
        MobileAds.initialize(getActivity(), initializationStatus -> {
            Log.d(TAG, "Google Mobile Ads SDK inicializado com sucesso!");
            // Mostrar banner automaticamente após 3 segundos
            getActivity().runOnUiThread(() -> {
                new android.os.Handler().postDelayed(() -> {
                    Log.d(TAG, "Auto-mostrando banner...");
                    showBannerAutomatic();
                }, 3000);
            });
        });
    }

    private void showBannerAutomatic() {
        try {
            if (bannerView == null) {
                Log.d(TAG, "Criando AdView automatico (fino no topo)...");
                bannerView = new AdView(getActivity());
                // Tamanho customizado: 80x80 (bem fino, 75% menos que normal)
                // Tamanho bem fino: 250x50 (reduzido, bem discreto no topo)
                bannerView.setAdSize(new AdSize(250, 50));
                bannerView.setAdUnitId(BANNER_AD_ID);

                bannerView.setAdListener(new AdListener() {
                    @Override
                    public void onAdLoaded() {
                        Log.d(TAG, ">>> ANUNCIO CARREGADO COM SUCESSO! <<<");
                        bannerView.setVisibility(View.VISIBLE);
                    }

                    @Override
                    public void onAdFailedToLoad(LoadAdError adError) {
                        Log.e(TAG, ">>> ERRO ao carregar anuncio: " + adError.getMessage());
                        Log.e(TAG, ">>> Codigo erro: " + adError.getCode());
                    }

                    @Override
                    public void onAdImpression() {
                        Log.d(TAG, "Impressao de anuncio registrada!");
                    }
                });

                ViewGroup webViewParent = (ViewGroup) getBridge().getWebView().getParent();
                FrameLayout.LayoutParams params = new FrameLayout.LayoutParams(
                    FrameLayout.LayoutParams.MATCH_PARENT,  // ocupar toda a largura
                    FrameLayout.LayoutParams.WRAP_CONTENT
                );
                // TOP | CENTER_HORIZONTAL = topo centralizado
                params.gravity = Gravity.TOP | Gravity.CENTER_HORIZONTAL;
                params.topMargin = 8; // pequeno espaço do topo
                webViewParent.addView(bannerView, params);
                Log.d(TAG, "AdView adicionado ao layout (TOPO CENTRALIZADO, 120x50)");
            }

            AdRequest adRequest = new AdRequest.Builder().build();
            bannerView.loadAd(adRequest);
            Log.d(TAG, "Requisicao de anuncio enviada!");
        } catch (Exception e) {
            Log.e(TAG, "ERRO ao mostrar banner automatico: " + e.getMessage(), e);
        }
    }

    @PluginMethod
    public void showBannerAd(PluginCall call) {
        Log.d(TAG, "showBannerAd chamado!");
        getActivity().runOnUiThread(() -> {
            try {
                if (bannerView == null) {
                    Log.d(TAG, "Criando AdView...");
                    bannerView = new AdView(getActivity());
                    // Use SMART_BANNER para um banner mais fino que se adapta ao tamanho
                bannerView.setAdSize(AdSize.SMART_BANNER);
                    bannerView.setAdUnitId(BANNER_AD_ID);

                    bannerView.setAdListener(new AdListener() {
                        @Override
                        public void onAdLoaded() {
                            Log.d(TAG, ">>> ANUNCIO CARREGADO COM SUCESSO! <<<");
                            bannerView.setVisibility(View.VISIBLE);
                        }

                        @Override
                        public void onAdFailedToLoad(LoadAdError adError) {
                            Log.e(TAG, ">>> ERRO ao carregar anuncio: " + adError.getMessage());
                            Log.e(TAG, ">>> Codigo erro: " + adError.getCode());
                            Log.e(TAG, ">>> Dominio: " + adError.getDomain());
                        }

                        @Override
                        public void onAdOpened() {
                            Log.d(TAG, "Anuncio aberto (clicado)");
                        }

                        @Override
                        public void onAdClicked() {
                            Log.d(TAG, "Anuncio clicado!");
                        }

                        @Override
                        public void onAdClosed() {
                            Log.d(TAG, "Anuncio fechado");
                        }

                        @Override
                        public void onAdImpression() {
                            Log.d(TAG, "Impressao de anuncio registrada!");
                        }
                    });

                    // Adicionar o banner ao layout da WebView
                    ViewGroup webViewParent = (ViewGroup) getBridge().getWebView().getParent();
                    FrameLayout.LayoutParams params = new FrameLayout.LayoutParams(
                        FrameLayout.LayoutParams.WRAP_CONTENT,
                        FrameLayout.LayoutParams.WRAP_CONTENT
                    );
                    params.gravity = Gravity.BOTTOM | Gravity.CENTER_HORIZONTAL;
                    webViewParent.addView(bannerView, params);
                    Log.d(TAG, "AdView adicionado ao layout (BOTTOM)");
                }

                Log.d(TAG, "Carregando anuncio com ID: " + BANNER_AD_ID);
                AdRequest adRequest = new AdRequest.Builder().build();
                bannerView.loadAd(adRequest);
                Log.d(TAG, "Requisicao de anuncio enviada!");

                call.resolve();
            } catch (Exception e) {
                Log.e(TAG, "ERRO em showBannerAd: " + e.getMessage(), e);
                call.reject("Failed to show banner ad: " + e.getMessage());
            }
        });
    }

    @PluginMethod
    public void hideBannerAd(PluginCall call) {
        getActivity().runOnUiThread(() -> {
            if (bannerView != null) {
                bannerView.setVisibility(View.GONE);
            }
            call.resolve();
        });
    }

    @PluginMethod
    public void removeBannerAd(PluginCall call) {
        getActivity().runOnUiThread(() -> {
            if (bannerView != null) {
                ViewGroup parent = (ViewGroup) bannerView.getParent();
                if (parent != null) {
                    parent.removeView(bannerView);
                }
                bannerView.destroy();
                bannerView = null;
            }
            call.resolve();
        });
    }
}
