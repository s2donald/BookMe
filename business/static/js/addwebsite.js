
var btnBookMe = document.querySelector('#BookMePlugin');
var BookMeUrl = btnBookMe.dataset.url
var color = btnBookMe.dataset.color
var DOM_img = document.createElement("img")
DOM_img.src = "https://django-gibele.s3.amazonaws.com/img/favicon/logo/BookMe-blackgrad.svg"
DOM_img.width = '50'

class BookmeModalConfig {
    // iframeUrl = 'https://hh5l.gibele.com:8000';
    iframeUrl = BookMeUrl
    buttonCallBookmeModalText = 'Book Now';
    poweredByBookMe = "Powered by"
    needInit = true;
    needLoadIframeOnInit = true;
    waitForLoadBeforeChangeModalState = false;
    closeOnBackdropClick = true;
    showCrossbar = true;

    constructor(obj) {
        if (obj) {
            Object.assign(this, obj);
        }
    }
}

class BookmeModal {
    modalContainerRef = null;
    initIframeInModal = null;
    iframeRef = null;
    buttonCallBookmeModalRef = null;
    config;

    constructor(config) {
        this.config = config;

        if (this.config.needInit) {
            this.init();
        }
    }

    init() {
        document.addEventListener('DOMContentLoaded', () => {
            this.modalContainerRef = this.createBookmeModal();
            document.body.insertBefore(this.modalContainerRef, document.body.firstChild);

            if (this.config.needLoadIframeOnInit) {
                const iframeRef = this.initIframeInModal();

                iframeRef.onload = () => {
                    this.config.iframeRef = iframeRef;
                };
            }

            this.createButtonCallBookmeModal();

            if (this.config.closeOnBackdropClick) {
                this.initWindowClickBackdrop();
            }
        });
    }

    initWindowClickBackdrop() {
        window.addEventListener('click', (event) => {
            if (this.modalContainerRef !== null && event.target === this.modalContainerRef) {
                this.hideModal();
            }
        });
    }
    isHexColor (hex) {
        return typeof hex === 'string'
            && hex.length === 6
            && !isNaN(Number('0x' + hex))
    }

    createBookmeModal() {
        const createModalContainer = () => {
            const element = document.createElement('div');
            const elementStyle = element.style;

            elementStyle.display = 'none';
            elementStyle.position = 'fixed';
            elementStyle.zIndex = '1';
            elementStyle.paddingTop = '4%';
            elementStyle.paddingBottom = '4%';
            elementStyle.left = '0';
            elementStyle.top = '0';
            elementStyle.width = '100%';
            elementStyle.height = '100%';
            elementStyle.overflow = 'auto';
            elementStyle.backgroundColor = 'rgba(0,0,0,0.4)';

            return element;
        };

        const modalContainer = createModalContainer();

        const createModalContent = () => {
            const element = document.createElement('div');

            const elementStyle = element.style;

            elementStyle.backgroundColor = '#e9e9e9';
            elementStyle.margin = 'auto';
            elementStyle.border = 'none';
            elementStyle.width = '80%';
            elementStyle.height = '80%';

            return element;
        };

        const modalContent = createModalContent();

        modalContainer.appendChild(modalContent);

        if (this.config.showCrossbar) {
            const createCrossbarButton = () => {
                const element = document.createElement('span');
                const elementStyle = element.style;

                elementStyle.color = '#aaaaaa';
                elementStyle.borderRadius = '16px';
                elementStyle.fontSize = '24px';
                elementStyle.fontWeight = 'bold';
                elementStyle.fontFamily = 'Arial, Helvetica, sans-serif';
                elementStyle.textDecoration = 'none';
                elementStyle.cursor = 'pointer';
                elementStyle.padding = '20px';
                elementStyle.position = 'block';

                element.onclick = () => {
                    if (this.modalContainerRef) {
                        this.hideModal();
                    }
                };

                const elementText = document.createTextNode('x');
                element.appendChild(elementText);

                return element;
            };

            const crossbarButton = createCrossbarButton();

            modalContent.appendChild(crossbarButton);
        }

        const createIframe = () => {
            const element = document.createElement('iframe');
            const elementStyle = element.style;

            elementStyle.width = '100%';
            elementStyle.height = '100%';
            elementStyle.border = 'none';

            element.src = this.config.iframeUrl;
            element.sandbox = 'allow-forms allow-popups allow-same-origin allow-scripts';

            return element;
        };

        this.initIframeInModal = () => {
            const iframe = createIframe();

            modalContent.appendChild(iframe);

            return iframe;
        }

        return modalContainer;
    }

    createButtonCallBookmeModal() {
        this.buttonCallBookmeModalRef = document.getElementById('BookMePlugin');
        this.buttonCallBookmeModalRef.appendChild(document.createTextNode(this.config.buttonCallBookmeModalText));
        this.buttonCallBookmeModalRef.appendChild(document.createElement("br"));
        this.buttonCallBookmeModalRef.appendChild(DOM_img);

        const mycolor = this.isHexColor(color);
        if (!mycolor){
            color = "ffae74"
        }
        const elementStyle = this.buttonCallBookmeModalRef.style;
        elementStyle.overflow = 'initial';
        elementStyle.zIndex = '9999999';
        elementStyle.border = 'none';
        elementStyle.borderRadius = '16px'
        elementStyle.paddingLeft = '28px';
        elementStyle.paddingRight = '28px';
        elementStyle.paddingTop = '14px';
        elementStyle.paddingBottom = '14px';
        elementStyle.textAlign = 'center';
        elementStyle.textDecoration = 'none';
        elementStyle.display = 'inline-block';
        elementStyle.fontSize = '16px';
        elementStyle.cursor = 'pointer';
        elementStyle.backgroundColor = '#'+color;

        this.buttonCallBookmeModalRef.onclick = () => {
            var windowWidth		=	jQuery(window).width();
            if( windowWidth < 600 )
            {
                window.open( BookMeUrl , '_blank' );
                return;
            }
            if (this.buttonCallBookmeModalRef.disabled) {
                return;
            }

            this.buttonCallBookmeModalRef.disabled = true;

            const changeModalState = () => {
                if (this.isModalOpened()) {
                    this.hideModal();
                } else {
                    this.showModal();
                }

                this.buttonCallBookmeModalRef.disabled = false;
            }

            if (this.config.waitForLoadBeforeChangeModalState && this.config.iframeRef === null) {
                this.config.iframeRef = this.initIframeInModal();
                this.config.iframeRef.onload = () => {
                    changeModalState();
                };
            } else {
                changeModalState();
            }

        };
    }

    hideModal() {
        this.modalContainerRef.style.display = 'none';
    }

    showModal() {
        this.modalContainerRef.style.display = 'block';
    }

    isModalOpened() {
        return this.modalContainerRef.style.display !== 'none';
    }
}

new BookmeModal(new BookmeModalConfig());
