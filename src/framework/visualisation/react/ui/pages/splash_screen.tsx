import React from 'react'
import { Weak } from '../../../../helpers'
import TextBundle from '../../../../text_bundle'
import { Translator } from '../../../../translator'
import { PropsUIPageSplashScreen } from '../../../../types/pages'
import { ReactFactoryContext } from '../../factory'
import { PrimaryButton } from '../elements/button'
import { CheckBox } from '../elements/check_box'
import { Label, Title1 } from '../elements/text'
import LogoSvg from '../../../../../assets/images/logo_uva.svg'
import { Footer } from './templates/footer'
import { Page } from './templates/page'
import { Sidebar } from './templates/sidebar'
import { Bullet } from '../elements/bullet'

interface Copy {
  title: string
  continueButton: string
  privacyLabel: string
}

type Props = Weak<PropsUIPageSplashScreen> & ReactFactoryContext

function prepareCopy ({ locale }: Props): Copy {
  return {
    title: Translator.translate(title, locale),
    continueButton: Translator.translate(continueButton, locale),
    privacyLabel: Translator.translate(privacyLabel, locale)
  }
}

export const SplashScreen = (props: Props): JSX.Element => {
  const [checked, setChecked] = React.useState<boolean>(false)
  const [waiting, setWaiting] = React.useState<boolean>(false)
  const { title, continueButton, privacyLabel } = prepareCopy(props)
  const { locale, resolve } = props

  function handleContinue (): void {
    if (checked && !waiting) {
      setWaiting(true)
      resolve?.({ __type__: 'PayloadVoid', value: undefined })
    }
  }

  function handleCheck (): void {
    setChecked(true)
  }

  function renderDescription (): JSX.Element {
    if (locale === 'nl') return nlDescription
    return enDescription
  }

  const enDescription: JSX.Element = (
    <>
      <div className='text-bodylarge font-body text-grey1'>
        <div className='mb-8 text-bodylarge font-body text-grey1'>
          Thank you for participating on the study <span style={{ fontWeight: 'bolder' }}>"Extraversion influence on social media posts, with focus in Instagram"</span> 
          and for donating you data as Data Download Packages (DDPs).
        </div>
        <div className='mb-8 text-bodylarge font-body text-grey1'>
        Watch the video below to understand what data donation is, and how <span style={{ fontWeight: 'bolder' }}>YOU</span> can help researchers
        </div>
        <div className='mb-8 text-bodylarge font-body text-grey1'>
          <iframe width="640" height="360" src="https://www.youtube.com/embed/O_kYejQIaK8?autoplay=0&mute=1"></iframe> 
        </div>
        <div className='mb-8 text-bodylarge font-body text-grey1'>
          Our reseachers are interrest on your Instagram data that need to be as a Data Download Package (zip file with all content provided by instagram).
          Please notice that it may take up to <span style={{ fontWeight: 'bolder' }}>14 days for Instagram to send you the data</span>.  
        </div>
        <div className='mb-8 text-bodylarge font-body text-grey1'>
        The video below instruct you how to request and recieve your personal data from Instagram.
        </div>
        <div className='mb-8 text-bodylarge font-body text-grey1'>
          <iframe width="640" height="360" src="https://www.youtube.com/embed/dPPXEefnviI?autoplay=0&mute=1"></iframe> 
        </div>
        
        <div className='mb-8 text-bodylarge font-body text-grey1'>
          We will walk you through this process step by step. Staring with 2 basic questions about yourself, 
          and during data loading, <span style={{ fontWeight: 'bolder' }}>NO</span> data is stored or sent to a server. 
          You can delete rows from the data before donating. Data will only be donated and stored when you click the button “Yes, donate” on the page that shows your data.
        </div>
        <div className='mb-8 text-bodylarge font-body text-grey1'>
          By clicking the button “<span className='font-bodybold'>Yes, donate</span>”:
        </div>
        <div className='flex flex-col gap-3 mb-8'>
          <Bullet>
            <div>you fully and voluntarily agree to donate your data for this research.</div>
          </Bullet>
          <Bullet>
            <div>you are aware that when your data is used for academic publications, or made publicly available in some other form, this will be anonymous.</div>
          </Bullet>
          <Bullet>
            <div>you are aware that you have the right to withdraw your permission.</div>
          </Bullet>
        </div>
        <div className='mb-10'>
          This website keeps cookies or anyother information  - for example on which pages of this website you click - as part of this research. More information can be found on our privacy page.
        </div>
      </div>
    </>
  )

  const nlDescription: JSX.Element = (
    <>
        <div className='text-bodylarge font-body text-grey1'>
        <div className='mb-8 text-bodylarge font-body text-grey1'>
          Thank you for participating on the study <span style={{ fontWeight: 'bolder' }}>"Extraversion influence on social media posts, with focus in Instagram"</span> 
          and for donating you data as Data Download Packages (DDPs).
        </div>
        <div className='mb-8 text-bodylarge font-body text-grey1'>
        Watch the video below to understand what data donation is, and how <span style={{ fontWeight: 'bolder' }}>YOU</span> can help researchers
        </div>
        <div className='mb-8 text-bodylarge font-body text-grey1'>
          <iframe width="640" height="360" src="https://www.youtube.com/embed/O_kYejQIaK8?autoplay=0&mute=1"></iframe> 
        </div>
        <div className='mb-8 text-bodylarge font-body text-grey1'>
          Our reseachers are interrest on your Instagram data that need to be as a Data Download Package (zip file with all content provided by instagram).
          Please notice that it may take up to <span style={{ fontWeight: 'bolder' }}>14 days for Instagram to send you the data</span>.  
        </div>
        <div className='mb-8 text-bodylarge font-body text-grey1'>
        The video below instruct you how to request and recieve your personal data from Instagram.
        </div>
        <div className='mb-8 text-bodylarge font-body text-grey1'>
          <iframe width="640" height="360" src="https://www.youtube.com/embed/dPPXEefnviI?autoplay=0&mute=1"></iframe> 
        </div>
        
        <div className='mb-8 text-bodylarge font-body text-grey1'>
          We will walk you through this process step by step. Staring with 2 basic questions about yourself, 
          and during data loading, <span style={{ fontWeight: 'bolder' }}>NO</span> data is stored or sent to a server. 
          You can delete rows from the data before donating. Data will only be donated and stored when you click the button “Yes, donate” on the page that shows your data.
        </div>
        <div className='mb-8 text-bodylarge font-body text-grey1'>
          By clicking the button “<span className='font-bodybold'>Yes, donate</span>”:
        </div>
        <div className='flex flex-col gap-3 mb-8'>
          <Bullet>
            <div>you fully and voluntarily agree to donate your data for this research.</div>
          </Bullet>
          <Bullet>
            <div>you are aware that when your data is used for academic publications, or made publicly available in some other form, this will be anonymous.</div>
          </Bullet>
          <Bullet>
            <div>you are aware that you have the right to withdraw your permission.</div>
          </Bullet>
        </div>
        <div className='mb-10'>
          This website keeps cookies or anyother information  - for example on which pages of this website you click - as part of this research. More information can be found on our privacy page.
        </div>
      </div>
    </>
  )

  const footer: JSX.Element = <Footer />

  const sidebar: JSX.Element = <Sidebar logo={LogoSvg} />

  const body: JSX.Element = (
    <>
      <Title1 text={title} />
      {renderDescription()}
      <div className='flex flex-col gap-8'>
        <div className='flex flex-row gap-4 items-center'>
          <CheckBox id='0' selected={checked} onSelect={() => handleCheck()} />
          <Label text={privacyLabel} />
        </div>
        <div className={`flex flex-row gap-4 ${checked ? '' : 'opacity-30'}`}>
          <PrimaryButton label={continueButton} onClick={handleContinue} enabled={checked} spinning={waiting} />
        </div>
      </div>
    </>
  )

  return (
    <Page
      body={body}
      sidebar={sidebar}
      footer={footer}
    />
  )
}

const title = new TextBundle()
  .add('en', 'Welcome')
  .add('nl', 'Welkom')

const continueButton = new TextBundle()
  .add('en', 'Start')
  .add('nl', 'Start')

const privacyLabel = new TextBundle()
  .add('en', 'I have read and agree with the above terms.')
  .add('nl', 'Ik heb deze voorwaarden gelezen en ben hiermee akkoord.')
